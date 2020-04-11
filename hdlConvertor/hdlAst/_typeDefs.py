from enum import Enum
from typing import Dict, Union, Tuple, List
from hdlConvertor.hdlAst._bases import iHdlObj,iHdlObjWithName

HdlTypeInt = int
HdlTypeStr = str
# Verilog real
HdlTypeFloat = float
HdlTypeEnum = Enum


class HdlSimpleRange(iHdlObj):
    """Simple range A:B, A to B, A DOWNTO B.
    """
    __slots__ = ["left", "dir", "right"]
    def __init__(self):
        super(HdlSimpleRange, self).__init__()
        self.left = None
        self.dir = None
        self.right = None

class HdlRange(iHdlObj):
    """Combined concept of an HDL range.

    The range may be defined as a subtype, (simple) range, or attribute with
    corresponding attributes.
    """
    __slots__ = ["subtype", "range", "attribute"]
    def __init__(self, subtype=None, rng=None, attribute=None):
        super(HdlRange, self).__init__()
        self.subtype = subtype
        self.range = rng
        self.attribute = attribute

class HdlSubtype(iHdlObj):
    """HDL subtype indication concept.

    A subtype indication is used pretty much any time an object is declared:
    generic/port/parameter declaration lists, variable and signal declarations,
    etc.

    """
    __slots__ = ["parent_type", "constraint"]
    def __init__(self, parent_type=None, constraint=None):
        super(HdlSubtype, self).__init__()
        self.parent_type = parent_type
        self.constraint = constraint

class HdlConstraint(iHdlObj):
    """HDL subtype constraint

    Represents any kind of constraint applied in an object declaration, port
    declaration, etc.
    """
    __slots__ = ["range", "indexes", "element", "field_cons"]
    def __init__(self):
        super(HdlConstraint, self).__init__()
        self.range = None
        self.indexes = []
        self.element = None
        self.field_cons = {}

class HdlTypeDec(iHdlObjWithName):
    """HDL type declaration

    HDL type declarations including array, record, struct, union, subtype,
    physical, access, file, etc.
    """
    __slots__ = ["subtype", "ids", "base_type", "isUnion", "indexes", "elem_type", "fields"]
    def __init__(self):
        super(HdlTypeDec, self).__init__()
        self.subtype = None
        self.ids = {}
        self.base_type = None
        self.isUnion = False
        self.indexes = None
        self.elem_type = None
        self.fields = {}

# arrays are described as HdlCall(HdlBuiltinFn.INDEX, (type, array size))
class HdlTypeBitsDef(iHdlObjWithName):
    """
    The type which represents bit or bit vector in HDL (std_logic/_vector
    in VHDL, [0:8] in Verilog )

    :ivar ~.states: 2 means that each bit can be 0 or 1
        4 - (0, 1, X, Z) (e.g. Verilog wire)
        9 - (0, 1, X, Z, U, W, L, H, -) (e.g. VHDL std_logic)
            'U': uninitialized. This signal hasn't been set yet.
            'X': unknown. Impossible to determine this value/result.
            '0': logic 0
            '1': logic 1
            'Z': High Impedance
            'W': Weak signal, can't tell if it should be 0 or 1.
            'L': Weak signal that should probably go to 0
            'H': Weak signal that should probably go to 1
            '-': Don't care.
    :note: in new you should let lsb=0, it is there only for legacy issues
    """
    STD_LOGIC_STATES = 9
    WIRE_STATES = 4
    __slots__ = ["name", "msb", "lsb", "signed", "is_bigendian", "states"]

    def __init__(self, msb, lsb=0, signed=False):
        super(HdlTypeBitsDef, self).__init__()
        self.msb = msb  # type: int
        self.lsb = lsb  # type: int
        self.signed = signed  # type: bool
        self.is_bigendian = False  # type: bool
        self.states = 2

    def width(self):
        if self.msb >= self.lsb:
            return self.msb - self.lsb
        else:
            return self.lsb - self.msb

    def __hash__(self):
        return hash((self.msb, self.lsb, self.signed, self.is_bigendian))

    def __eq__(self, other):
        return isinstance(other, HdlTypeBitsDef) and (
            self.msb == other.msb
            and self.lsb == other.lsb
            and self.signed == other.signed
            and self.is_bigendian == other.is_bigendian)


class HdlClassDef(iHdlObjWithName):
    """
    Definition of SystemVerilog class/struct/interface or VHDL record

    :note: name may be None

    """
    __slots__ = ["name", "parents", "is_virtual", "is_static",
                 "is_struct", "is_union", "is_interface",
                 "private", "public", "protected"]

    def __init__(self):
        super(HdlClassDef, self).__init__()
        self.parents = []  # type: List[iHdlExpr]
        self.is_virtual = False  # type: bool
        self.is_static = False  # type: bool
        self.is_struct = False  # type: bool
        self.is_union = False  # type: bool
        self.private = []  # type: List[iHdlObj]
        self.public = []  # type: List[iHdlObj]
        self.protected = []  # type: List[iHdlObj]


class HdlEnumDef(iHdlObjWithName):
    """
    Definition of VHDL Enumeration Type or SystemVerilog enum

    :note: name may be None
    """
    __slots__ = ["name", "values"]

    def __init__(self):
        super(HdlEnumDef, self).__init__()
        self.values = []  # type: List[Union[str, Tuple[str, int]]]
