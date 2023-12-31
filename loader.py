from yaml.reader import *
from yaml.scanner import *
from yaml.parser import *
from yaml.constructor import *
from yaml.resolver import *
from yaml.events import *
from yaml.tokens import *
from yaml.composer import ComposerError

from discopy.frobenius import Hypergraph as H, Id, Ob, Ty, Box, Spider

class HypergraphComposer:

    def __init__(self):
        self.anchors = {}

    def check_node(self):
        # Drop the STREAM-START event.
        if self.check_event(StreamStartEvent):
            self.get_event()

        # If there are more documents available?
        return not self.check_event(StreamEndEvent)

    def get_node(self):
        # Get the root node of the next document.
        if not self.check_event(StreamEndEvent):
            return self.compose_document()

    def get_single_node(self):
        # Drop the STREAM-START event.
        self.get_event()

        # Compose a document if the stream is not empty.
        document = None
        if not self.check_event(StreamEndEvent):
            document = self.compose_document()

        # Ensure that the stream contains no more documents.
        if not self.check_event(StreamEndEvent):
            event = self.get_event()
            raise ComposerError("expected a single document in the stream",
                    document.start_mark, "but found another document",
                    event.start_mark)

        # Drop the STREAM-END event.
        self.get_event()

        return document

    def compose_document(self):
        # Drop the DOCUMENT-START event.
        self.get_event()

        # Compose the root node.
        node = self.compose_node(None, None)

        # Drop the DOCUMENT-END event.
        self.get_event()

        self.anchors = {}
        return node

    def compose_node(self, parent, index):
        if self.check_event(AliasEvent):
            event = self.get_event()
            anchor = event.anchor
            if anchor not in self.anchors:
                raise ComposerError(None, None, "found undefined alias %r"
                        % anchor, event.start_mark)
            return self.anchors[anchor]
        event = self.peek_event()
        anchor = event.anchor
        if anchor is not None:
            if anchor in self.anchors:
                raise ComposerError("found duplicate anchor %r; first occurrence"
                        % anchor, self.anchors[anchor].start_mark,
                        "second occurrence", event.start_mark)
        self.descend_resolver(parent, index)
        if self.check_event(ScalarEvent):
            node = self.compose_scalar_node(anchor)
        elif self.check_event(SequenceStartEvent):
            node = self.compose_sequence_node(anchor)
        elif self.check_event(MappingStartEvent):
            node = self.compose_mapping_node(anchor)
        self.ascend_resolver()
        return node

    def compose_scalar_node(self, anchor):
        event = self.get_event()
        tag = event.tag
        if tag is None or tag == '!':
            tag = self.DEFAULT_SCALAR_TAG
        # node = H.id(Ty(str(event.value))) \
        #     if event.value != "" else H.id()
        node = H.from_box(Box(str(event.value), Ty(str(event.value)), Ty(str(event.value)))) \
            if event.value != "" else H.id()
        if anchor is not None:
            self.anchors[anchor] = node
        return node

    def compose_sequence_node(self, anchor):
        start_event = self.get_event()
        tag = start_event.tag
        if tag is None or tag == '!':
            tag = self.DEFAULT_SEQUENCE_TAG
        node = H.id()
        # node = SequenceNode(tag, [],
        #         start_event.start_mark, None,
        #         flow_style=start_event.flow_style)
        if anchor is not None:
            self.anchors[anchor] = node
        index = 0
        while not self.check_event(SequenceEndEvent):
            item = self.compose_node(node, index)
            node = compose_entry(node, item)
            index += 1
        end_event = self.get_event()
        node.end_mark = end_event.end_mark
        return node


    def compose_mapping_node(self, anchor):
        start_event = self.get_event()
        tag = start_event.tag
        if tag is None or tag == '!':
            tag = self.DEFAULT_MAPPING_TAG
        node = H.id()#Ty(str(start_event.start_mark)))
        if anchor is not None:
            self.anchors[anchor] = node
        while not self.check_event(MappingEndEvent):
            item_key = self.compose_node(node, None)
            item_value = self.compose_node(node, item_key)
            kv = compose_entry(item_key, item_value)
            node @= kv
        end_event = self.get_event()
        node.end_mark = end_event.end_mark
        return node

def compose_entry(k, v):
    if len(v.cod + v.dom) == 0:
        return k
    spider_types = tuple(sorted(set(x.name for x in set(k.spider_types + v.spider_types))))
    g = H(
        dom=k.cod, cod=v.dom,
        boxes=(),
        wires=(
            k.cod.inside, # input wires of the hypergraph
            (),#tuple(((s,),(s,)) for s in spider_types),
            v.dom.inside, # input wires of the hypergraph
        ),
        spider_types={Ob(s): Ty(Ob(s)) for s in spider_types},
    )
    entry = k >> g >> v
    # g.to_diagram().draw()
    return entry


class HypergraphLoader(Reader, Scanner, Parser, HypergraphComposer, SafeConstructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        HypergraphComposer.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)

