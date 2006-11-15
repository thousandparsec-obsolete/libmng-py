
#define MNG_FALSE 0
MNG_FALSE = 0
#define MNG_TRUE  1
MNG_TRUE = 1
#define MNG_NULL  0
MNG_NULL = None

# ************************************************************************** 
# *                                                                        * 
# * Error-code structure                                                   * 
# *                                                                        * 
# * 0b0000 00xx xxxx xxxx - basic errors; severity 9 (environment)         * 
# * 0b0000 01xx xxxx xxxx - chunk errors; severity 9 (image induced)       * 
# * 0b0000 10xx xxxx xxxx - severity 5 errors (application induced)        * 
# * 0b0001 00xx xxxx xxxx - severity 2 warnings (recoverable)              * 
# * 0b0010 00xx xxxx xxxx - severity 1 warnings (recoverable)              * 
# *                                                                        * 
# ************************************************************************** 

MNG_NOERROR           = 0    # er.. indicates all's well   

MNG_OUTOFMEMORY       = 1    # oops, buy some megabytes!   
MNG_INVALIDHANDLE     = 2    # call mng_initialize first   
MNG_NOCALLBACK        = 3    # set the callbacks please    
MNG_UNEXPECTEDEOF     = 4    # what'd ya do with the data? 
MNG_ZLIBERROR         = 5    # zlib burped                 
MNG_JPEGERROR         = 6    # jpglib complained           
MNG_LCMSERROR         = 7    # little cms stressed out     
MNG_NOOUTPUTPROFILE   = 8    # no output-profile defined   
MNG_NOSRGBPROFILE     = 9    # no sRGB-profile defined     
MNG_BUFOVERFLOW       = 10   # zlib output-buffer overflow 
MNG_FUNCTIONINVALID   = 11   # ay, totally inappropriate   
MNG_OUTPUTERROR       = 12   # disk full ?                 
MNG_JPEGBUFTOOSMALL   = 13   # can't handle buffer overflow
MNG_NEEDMOREDATA      = 14   # I'm hungry, give me more    
MNG_NEEDTIMERWAIT     = 15   # Sleep a while then wake me  
MNG_NEEDSECTIONWAIT   = 16   # just processed a SEEK       
MNG_LOOPWITHCACHEOFF  = 17   # LOOP when playback info off 

MNG_DLLNOTLOADED      = 99   # late binding failed         

MNG_APPIOERROR        = 901  # application I/O error       
MNG_APPTIMERERROR     = 902  # application timing error    
MNG_APPCMSERROR       = 903  # application CMS error       
MNG_APPMISCERROR      = 904  # application other error     
MNG_APPTRACEABORT     = 905  # application aborts on trace 

MNG_INTERNALERROR     = 999  # internal inconsistancy      

MNG_INVALIDSIG        = 1025 # invalid graphics file       
MNG_INVALIDCRC        = 1027 # crc check failed            
MNG_INVALIDLENGTH     = 1028 # chunklength mystifies me    
MNG_SEQUENCEERROR     = 1029 # invalid chunk sequence      
MNG_CHUNKNOTALLOWED   = 1030 # completely out-of-place     
MNG_MULTIPLEERROR     = 1031 # only one occurence allowed  
MNG_PLTEMISSING       = 1032 # indexed-color requires PLTE 
MNG_IDATMISSING       = 1033 # IHDR-block requires IDAT    
MNG_CANNOTBEEMPTY     = 1034 # must contain some data      
MNG_GLOBALLENGTHERR   = 1035 # global data incorrect       
MNG_INVALIDBITDEPTH   = 1036 # bitdepth out-of-range       
MNG_INVALIDCOLORTYPE  = 1037 # colortype out-of-range      
MNG_INVALIDCOMPRESS   = 1038 # compression method invalid  
MNG_INVALIDFILTER     = 1039 # filter method invalid       
MNG_INVALIDINTERLACE  = 1040 # interlace method invalid    
MNG_NOTENOUGHIDAT     = 1041 # ran out of compressed data  
MNG_PLTEINDEXERROR    = 1042 # palette-index out-of-range  
MNG_NULLNOTFOUND      = 1043 # couldn't find null-separator
MNG_KEYWORDNULL       = 1044 # keyword cannot be empty     
MNG_OBJECTUNKNOWN     = 1045 # the object can't be found   
MNG_OBJECTEXISTS      = 1046 # the object already exists   
MNG_TOOMUCHIDAT       = 1047 # got too much compressed data
MNG_INVSAMPLEDEPTH    = 1048 # sampledepth out-of-range    
MNG_INVOFFSETSIZE     = 1049 # invalid offset-size         
MNG_INVENTRYTYPE      = 1050 # invalid entry-type          
MNG_ENDWITHNULL       = 1051 # may not end with NULL       
MNG_INVIMAGETYPE      = 1052 # invalid image_type          
MNG_INVDELTATYPE      = 1053 # invalid delta_type          
MNG_INVALIDINDEX      = 1054 # index-value invalid         
MNG_TOOMUCHJDAT       = 1055 # got too much compressed data
MNG_JPEGPARMSERR      = 1056 # JHDR/JPEG parms do not match
MNG_INVFILLMETHOD     = 1057 # invalid fill_method         
MNG_OBJNOTCONCRETE    = 1058 # object must be concrete     
MNG_TARGETNOALPHA     = 1059 # object has no alpha-channel 
MNG_MNGTOOCOMPLEX     = 1060 # can't handle complexity     
MNG_UNKNOWNCRITICAL   = 1061 # unknown critical chunk found
MNG_UNSUPPORTEDNEED   = 1062 # nEED requirement unsupported
MNG_INVALIDDELTA      = 1063 # Delta operation illegal     
MNG_INVALIDMETHOD     = 1064 # invalid MAGN method         
MNG_IMPROBABLELENGTH  = 1065 # impropable chunk length     
MNG_INVALIDBLOCK      = 1066 # invalid delta block         
MNG_INVALIDEVENT      = 1067 # invalid event_type          
MNG_INVALIDMASK       = 1068 # invalid mask_type           
MNG_NOMATCHINGLOOP    = 1069 # ENDL without matching LOOP  
MNG_SEEKNOTFOUND      = 1070 # EvNT points to unknown SEEK 
MNG_OBJNOTABSTRACT    = 1071 # object must be abstract     
MNG_TERMSEQERROR      = 1072 # TERM in wrong place         
MNG_INVALIDFIELDVAL   = 1073 # invalid fieldvalue (generic)

MNG_INVALIDCNVSTYLE   = 2049 # can't make anything of this 
MNG_WRONGCHUNK        = 2050 # accessing the wrong chunk   
MNG_INVALIDENTRYIX    = 2051 # accessing the wrong entry   
MNG_NOHEADER          = 2052 # must have had header first  
MNG_NOCORRCHUNK       = 2053 # can't find parent chunk     
MNG_NOMHDR            = 2054 # no MNG header available     

MNG_IMAGETOOLARGE     = 4097 # input-image way too big     
MNG_NOTANANIMATION    = 4098 # file not a MNG              
MNG_FRAMENRTOOHIGH    = 4099 # frame-nr out-of-range       
MNG_LAYERNRTOOHIGH    = 4100 # layer-nr out-of-range       
MNG_PLAYTIMETOOHIGH   = 4101 # playtime out-of-range       
MNG_FNNOTIMPLEMENTED  = 4102 # function not yet available  

MNG_IMAGEFROZEN       = 8193 # stopped displaying          

MNG_LCMS_NOHANDLE     = 1                 # LCMS returned NULL handle 
MNG_LCMS_NOMEM        = 2                 # LCMS returned NULL gammatab 
MNG_LCMS_NOTRANS      = 3                 # LCMS returned NULL transform

# ************************************************************************** 
# *                                                                        * 
# *  Canvas styles                                                         * 
# *                                                                        * 
# *  Note that the intentions are pretty darn good, but that the focus     * 
# *  is currently on 8-bit color support                                   * 
# *                                                                        * 
# *  The RGB8_A8 style is defined for apps that require a separate         * 
# *  canvas for the color-planes and the alpha-plane (eg. mozilla)         * 
# *  This requires for the app to supply the "getalphaline" callback!!!    * 
# *                                                                        * 
# ************************************************************************** 


MNG_CANVAS_RGB8      = 0x00000000L
MNG_CANVAS_RGBA8     = 0x00001000L
MNG_CANVAS_RGBA8_PM  = 0x00009000L
MNG_CANVAS_ARGB8     = 0x00003000L
MNG_CANVAS_ARGB8_PM  = 0x0000B000L
MNG_CANVAS_RGB8_A8   = 0x00005000L
MNG_CANVAS_BGR8      = 0x00000001L
MNG_CANVAS_BGRX8     = 0x00010001L
MNG_CANVAS_BGRA8     = 0x00001001L
MNG_CANVAS_BGRA8PM   = 0x00009001L         # backward compatibility 
MNG_CANVAS_BGRA8_PM  = 0x00009001L
MNG_CANVAS_ABGR8     = 0x00003001L
MNG_CANVAS_ABGR8_PM  = 0x0000B001L
MNG_CANVAS_RGB16     = 0x00000100L         # not supported yet 
MNG_CANVAS_RGBA16    = 0x00001100L         # not supported yet 
MNG_CANVAS_ARGB16    = 0x00003100L         # not supported yet 
MNG_CANVAS_BGR16     = 0x00000101L         # not supported yet 
MNG_CANVAS_BGRA16    = 0x00001101L         # not supported yet 
MNG_CANVAS_ABGR16    = 0x00003101L         # not supported yet 
MNG_CANVAS_GRAY8     = 0x00000002L         # not supported yet 
MNG_CANVAS_GRAY16    = 0x00000102L         # not supported yet 
MNG_CANVAS_GRAYA8    = 0x00001002L         # not supported yet 
MNG_CANVAS_GRAYA16   = 0x00001102L         # not supported yet 
MNG_CANVAS_AGRAY8    = 0x00003002L         # not supported yet 
MNG_CANVAS_AGRAY16   = 0x00003102L         # not supported yet 
MNG_CANVAS_DX15      = 0x00000003L         # not supported yet 
MNG_CANVAS_DX16      = 0x00000004L         # not supported yet 

MNG_CANVAS_RGB565    = 0x00000005L
MNG_CANVAS_RGBA565   = 0x00001005L
MNG_CANVAS_BGR565    = 0x00000006L
MNG_CANVAS_BGRA565   = 0x00001006L
MNG_CANVAS_BGR565_A8 = 0x00004006L

BITSPERPIXEL = {
	MNG_CANVAS_RGB8:		8*3,
	MNG_CANVAS_RGBA8:		8*4,
	MNG_CANVAS_RGBA8_PM:	8*4,
	MNG_CANVAS_ARGB8:		8*4,
	MNG_CANVAS_ARGB8_PM:	8*4,
	MNG_CANVAS_RGB8_A8:		(8*3, 8*1),	# A8 has a seperated alpha channel
	MNG_CANVAS_BGR8:		8*3,
	MNG_CANVAS_BGRX8:		8*4,
	MNG_CANVAS_BGRA8:		8*4,
	MNG_CANVAS_BGRA8PM:		8*4,
	MNG_CANVAS_BGRA8_PM:	8*4,
	MNG_CANVAS_ABGR8:		8*4,
	MNG_CANVAS_ABGR8_PM:	8*4,
	MNG_CANVAS_RGB16:		8*3,
	MNG_CANVAS_RGBA16:		8*4,
	MNG_CANVAS_ARGB16:		8*4,
	MNG_CANVAS_BGR16:		8*3,
	MNG_CANVAS_BGRA16:		8*4,
	MNG_CANVAS_ABGR16:		8*4,
	MNG_CANVAS_GRAY8:		8*1,
	MNG_CANVAS_GRAY16:		8*2,
	MNG_CANVAS_GRAYA8:		(8*1, 8),
	MNG_CANVAS_GRAYA16:		(8*2, 8),
	MNG_CANVAS_AGRAY8:		8+8,
	MNG_CANVAS_AGRAY16:		8+16,
	MNG_CANVAS_DX15:		"Unknown",
	MNG_CANVAS_DX16:		"Unknown",
	MNG_CANVAS_RGB565:		5+6+5,
	MNG_CANVAS_RGBA565:		5+6+5+8,
	MNG_CANVAS_BGR565:		5+6+5,
	MNG_CANVAS_BGRA565:		5+6+5+8,
	MNG_CANVAS_BGR565_A8:	(5+6+5, 8),
}

def MNG_CANVAS_PIXELTYPE(C):
	return  (C & 0x000000FFL)
def MNG_CANVAS_BITDEPTH(C):
	return  (C & 0x00000100L)
def MNG_CANVAS_HASALPHA(C):
	return  (C & 0x00001000L)
def MNG_CANVAS_ALPHAFIRST(C):
	return  (C & 0x00002000L)
def MNG_CANVAS_ALPHASEPD(C):
	return  (C & 0x00004000L)
def MNG_CANVAS_ALPHAPM(C):
	return  (C & 0x00008000L)
def MNG_CANVAS_HASFILLER(C):
	return  (C & 0x00010000L)

def MNG_CANVAS_RGB(C):
	return  (MNG_CANVAS_PIXELTYPE(C) == 0)
def MNG_CANVAS_BGR(C):
	return  (MNG_CANVAS_PIXELTYPE(C) == 1)
def MNG_CANVAS_GRAY(C):
	return  (MNG_CANVAS_PIXELTYPE(C) == 2)
def MNG_CANVAS_DIRECTX15(C):
	return  (MNG_CANVAS_PIXELTYPE(C) == 3)
def MNG_CANVAS_DIRECTX16(C):
	return  (MNG_CANVAS_PIXELTYPE(C) == 4)
def MNG_CANVAS_RGB_565(C):
	return  (MNG_CANVAS_PIXELTYPE(C) == 5)
def MNG_CANVAS_BGR_565(C):
	return  (MNG_CANVAS_PIXELTYPE(C) == 6)
def MNG_CANVAS_8BIT(C):
	return (~MNG_CANVAS_BITDEPTH(C))
def MNG_CANVAS_16BIT(C):
	return  (MNG_CANVAS_BITDEPTH(C))
def MNG_CANVAS_PIXELFIRST(C):
	return (~MNG_CANVAS_ALPHAFIRST(C))

# **************************************************************************
# *                                                                        *
# *  Chunk names (idea adapted from libpng 1.1.0 - png.h)                  *
# *                                                                        *
# **************************************************************************

MNG_UINT_HUH  = 0x40404040L

MNG_UINT_BACK = 0x4241434bL
MNG_UINT_BASI = 0x42415349L
MNG_UINT_CLIP = 0x434c4950L
MNG_UINT_CLON = 0x434c4f4eL
MNG_UINT_DBYK = 0x4442594bL
MNG_UINT_DEFI = 0x44454649L
MNG_UINT_DHDR = 0x44484452L
MNG_UINT_DISC = 0x44495343L
MNG_UINT_DROP = 0x44524f50L
MNG_UINT_ENDL = 0x454e444cL
MNG_UINT_FRAM = 0x4652414dL
MNG_UINT_IDAT = 0x49444154L
MNG_UINT_IEND = 0x49454e44L
MNG_UINT_IHDR = 0x49484452L
MNG_UINT_IJNG = 0x494a4e47L
MNG_UINT_IPNG = 0x49504e47L
MNG_UINT_JDAA = 0x4a444141L
MNG_UINT_JDAT = 0x4a444154L
MNG_UINT_JHDR = 0x4a484452L
MNG_UINT_JSEP = 0x4a534550L
MNG_UINT_JdAA = 0x4a644141L
MNG_UINT_LOOP = 0x4c4f4f50L
MNG_UINT_MAGN = 0x4d41474eL
MNG_UINT_MEND = 0x4d454e44L
MNG_UINT_MHDR = 0x4d484452L
MNG_UINT_MOVE = 0x4d4f5645L
MNG_UINT_ORDR = 0x4f524452L
MNG_UINT_PAST = 0x50415354L
MNG_UINT_PLTE = 0x504c5445L
MNG_UINT_PPLT = 0x50504c54L
MNG_UINT_PROM = 0x50524f4dL
MNG_UINT_SAVE = 0x53415645L
MNG_UINT_SEEK = 0x5345454bL
MNG_UINT_SHOW = 0x53484f57L
MNG_UINT_TERM = 0x5445524dL
MNG_UINT_bKGD = 0x624b4744L
MNG_UINT_cHRM = 0x6348524dL
MNG_UINT_eXPI = 0x65585049L
MNG_UINT_fPRI = 0x66505249L
MNG_UINT_gAMA = 0x67414d41L
MNG_UINT_hIST = 0x68495354L
MNG_UINT_iCCP = 0x69434350L
MNG_UINT_iTXt = 0x69545874L
MNG_UINT_nEED = 0x6e454544L
MNG_UINT_oFFs = 0x6f464673L
MNG_UINT_pCAL = 0x7043414cL
MNG_UINT_pHYg = 0x70444167L
MNG_UINT_pHYs = 0x70485973L
MNG_UINT_sBIT = 0x73424954L
MNG_UINT_sCAL = 0x7343414cL
MNG_UINT_sPLT = 0x73504c54L
MNG_UINT_sRGB = 0x73524742L
MNG_UINT_tEXt = 0x74455874L
MNG_UINT_tIME = 0x74494d45L
MNG_UINT_tRNS = 0x74524e53L
MNG_UINT_zTXt = 0x7a545874L

MNG_UINT_evNT = 0x65764e54L

# **************************************************************************
# *                                                                        *
# *  Chunk property values                                                 *
# *                                                                        *
# **************************************************************************

MNG_BITDEPTH_1                   = 1     # IHDR, BASI, JHDR, PROM
MNG_BITDEPTH_2                   = 2
MNG_BITDEPTH_4                   = 4
MNG_BITDEPTH_8                   = 8     # sPLT
MNG_BITDEPTH_16                  = 16

MNG_COLORTYPE_GRAY               = 0     # IHDR, BASI, PROM
MNG_COLORTYPE_RGB                = 2
MNG_COLORTYPE_INDEXED            = 3
MNG_COLORTYPE_GRAYA              = 4
MNG_COLORTYPE_RGBA               = 6

MNG_COMPRESSION_DEFLATE          = 0     # IHDR, zTXt, iTXt, iCCP, BASI, JHDR

MNG_FILTER_ADAPTIVE              = 0     # IHDR, BASI, JHDR 
MNG_FILTER_NO_ADAPTIVE           = 1
MNG_FILTER_NO_DIFFERING          = 0
MNG_FILTER_DIFFERING             = 0x40
MNG_FILTER_MASK                  = MNG_FILTER_NO_ADAPTIVE | MNG_FILTER_DIFFERING
MNG_FILTER_DIFFERING             = 0xC0
MNG_FILTER_NOFILTER              = 0xC1

MNG_INTERLACE_NONE               = 0      # IHDR, BASI, JHDR
MNG_INTERLACE_ADAM7              = 1

MNG_FILTER_NONE                  = 0        # IDAT
MNG_FILTER_SUB                   = 1
MNG_FILTER_UP                    = 2
MNG_FILTER_AVERAGE               = 3
MNG_FILTER_PAETH                 = 4

MNG_INTENT_PERCEPTUAL            = 0             # sRGB
MNG_INTENT_RELATIVECOLORIMETRIC  = 1
MNG_INTENT_SATURATION            = 2
MNG_INTENT_ABSOLUTECOLORIMETRIC  = 3
                                                 # tEXt, zTXt, iTXt
MNG_TEXT_TITLE                   = "Title"
MNG_TEXT_AUTHOR                  = "Author"
MNG_TEXT_DESCRIPTION             = "Description"
MNG_TEXT_COPYRIGHT               = "Copyright"
MNG_TEXT_CREATIONTIME            = "Creation = Time"
MNG_TEXT_SOFTWARE                = "Software"
MNG_TEXT_DISCLAIMER              = "Disclaimer"
MNG_TEXT_WARNING                 = "Warning"
MNG_TEXT_SOURCE                  = "Source"
MNG_TEXT_COMMENT                 = "Comment"

MNG_FLAG_UNCOMPRESSED            = 0             # iTXt
MNG_FLAG_COMPRESSED              = 1

MNG_UNIT_UNKNOWN                 = 0             # pHYs, pHYg
MNG_UNIT_METER                   = 1
                                                 # MHDR
MNG_SIMPLICITY_VALID             = 0x00000001
MNG_SIMPLICITY_SIMPLEFEATURES    = 0x00000002
MNG_SIMPLICITY_COMPLEXFEATURES   = 0x00000004
MNG_SIMPLICITY_TRANSPARENCY      = 0x00000008
MNG_SIMPLICITY_JNG               = 0x00000010
MNG_SIMPLICITY_DELTAPNG          = 0x00000020

MNG_TERMINATION_DECODER_NC       = 0             # LOOP
MNG_TERMINATION_USER_NC          = 1
MNG_TERMINATION_EXTERNAL_NC      = 2
MNG_TERMINATION_DETERMINISTIC_NC = 3
MNG_TERMINATION_DECODER_C        = 4
MNG_TERMINATION_USER_C           = 5
MNG_TERMINATION_EXTERNAL_C       = 6
MNG_TERMINATION_DETERMINISTIC_C  = 7

MNG_DONOTSHOW_VISIBLE            = 0       # DEFI
MNG_DONOTSHOW_NOTVISIBLE         = 1

MNG_ABSTRACT                     = 0       # DEFI
MNG_CONCRETE                     = 1

MNG_NOTVIEWABLE                  = 0       # BASI
MNG_VIEWABLE                     = 1

MNG_FULL_CLONE                   = 0       # CLON
MNG_PARTIAL_CLONE                = 1
MNG_RENUMBER                     = 2

MNG_CONCRETE_ASPARENT            = 0       # CLON
MNG_CONCRETE_MAKEABSTRACT        = 1

MNG_LOCATION_ABSOLUTE            = 0       # CLON, MOVE
MNG_LOCATION_RELATIVE            = 1

MNG_TARGET_ABSOLUTE              = 0       # PAST
MNG_TARGET_RELATIVE_SAMEPAST     = 1
MNG_TARGET_RELATIVE_PREVPAST     = 2

MNG_COMPOSITE_OVER               = 0       # PAST
MNG_COMPOSITE_REPLACE            = 1
MNG_COMPOSITE_UNDER              = 2

MNG_ORIENTATION_SAME             = 0       # PAST
MNG_ORIENTATION_180DEG           = 2
MNG_ORIENTATION_FLIPHORZ         = 4
MNG_ORIENTATION_FLIPVERT         = 6
MNG_ORIENTATION_TILED            = 8

MNG_OFFSET_ABSOLUTE              = 0       # PAST
MNG_OFFSET_RELATIVE              = 1

MNG_BOUNDARY_ABSOLUTE            = 0       # PAST, FRAM
MNG_BOUNDARY_RELATIVE            = 1

MNG_BACKGROUNDCOLOR_MANDATORY    = 0x01    # BACK
MNG_BACKGROUNDIMAGE_MANDATORY    = 0x02    # BACK

MNG_BACKGROUNDIMAGE_NOTILE       = 0       # BACK
MNG_BACKGROUNDIMAGE_TILE         = 1

MNG_FRAMINGMODE_NOCHANGE         = 0       # FRAM
MNG_FRAMINGMODE_1                = 1
MNG_FRAMINGMODE_2                = 2
MNG_FRAMINGMODE_3                = 3
MNG_FRAMINGMODE_4                = 4

MNG_CHANGEDELAY_NO               = 0       # FRAM
MNG_CHANGEDELAY_NEXTSUBFRAME     = 1
MNG_CHANGEDELAY_DEFAULT          = 2

MNG_CHANGETIMOUT_NO              = 0       # FRAM
MNG_CHANGETIMOUT_DETERMINISTIC_1 = 1
MNG_CHANGETIMOUT_DETERMINISTIC_2 = 2
MNG_CHANGETIMOUT_DECODER_1       = 3
MNG_CHANGETIMOUT_DECODER_2       = 4
MNG_CHANGETIMOUT_USER_1          = 5
MNG_CHANGETIMOUT_USER_2          = 6
MNG_CHANGETIMOUT_EXTERNAL_1      = 7
MNG_CHANGETIMOUT_EXTERNAL_2      = 8

MNG_CHANGECLIPPING_NO            = 0       # FRAM
MNG_CHANGECLIPPING_NEXTSUBFRAME  = 1
MNG_CHANGECLIPPING_DEFAULT       = 2

MNG_CHANGESYNCID_NO              = 0       # FRAM
MNG_CHANGESYNCID_NEXTSUBFRAME    = 1
MNG_CHANGESYNCID_DEFAULT         = 2

MNG_CLIPPING_ABSOLUTE            = 0       # CLIP
MNG_CLIPPING_RELATIVE            = 1

MNG_SHOWMODE_0                   = 0       # SHOW
MNG_SHOWMODE_1                   = 1
MNG_SHOWMODE_2                   = 2
MNG_SHOWMODE_3                   = 3
MNG_SHOWMODE_4                   = 4
MNG_SHOWMODE_5                   = 5
MNG_SHOWMODE_6                   = 6
MNG_SHOWMODE_7                   = 7

MNG_TERMACTION_LASTFRAME         = 0       # TERM
MNG_TERMACTION_CLEAR             = 1
MNG_TERMACTION_FIRSTFRAME        = 2
MNG_TERMACTION_REPEAT            = 3

MNG_ITERACTION_LASTFRAME         = 0       # TERM
MNG_ITERACTION_CLEAR             = 1
MNG_ITERACTION_FIRSTFRAME        = 2

MNG_SAVEOFFSET_4BYTE             = 4       # SAVE
MNG_SAVEOFFSET_8BYTE             = 8

MNG_SAVEENTRY_SEGMENTFULL        = 0       # SAVE
MNG_SAVEENTRY_SEGMENT            = 1
MNG_SAVEENTRY_SUBFRAME           = 2
MNG_SAVEENTRY_EXPORTEDIMAGE      = 3

MNG_PRIORITY_ABSOLUTE            = 0       # fPRI
MNG_PRIORITY_RELATIVE            = 1

MNG_COLORTYPE_JPEGGRAY           = 8       # JHDR
MNG_COLORTYPE_JPEGCOLOR          = 10
MNG_COLORTYPE_JPEGGRAYA          = 12
MNG_COLORTYPE_JPEGCOLORA         = 14

MNG_BITDEPTH_JPEG8               = 8       # JHDR
MNG_BITDEPTH_JPEG12              = 12
MNG_BITDEPTH_JPEG8AND12          = 20

MNG_COMPRESSION_BASELINEJPEG     = 8       # JHDR

MNG_INTERLACE_SEQUENTIAL         = 0       # JHDR
MNG_INTERLACE_PROGRESSIVE        = 8

MNG_IMAGETYPE_UNKNOWN            = 0       # DHDR
MNG_IMAGETYPE_PNG                = 1
MNG_IMAGETYPE_JNG                = 2

MNG_DELTATYPE_REPLACE            = 0       # DHDR
MNG_DELTATYPE_BLOCKPIXELADD      = 1
MNG_DELTATYPE_BLOCKALPHAADD      = 2
MNG_DELTATYPE_BLOCKCOLORADD      = 3
MNG_DELTATYPE_BLOCKPIXELREPLACE  = 4
MNG_DELTATYPE_BLOCKALPHAREPLACE  = 5
MNG_DELTATYPE_BLOCKCOLORREPLACE  = 6
MNG_DELTATYPE_NOCHANGE           = 7

MNG_FILLMETHOD_LEFTBITREPLICATE  = 0       # PROM
MNG_FILLMETHOD_ZEROFILL          = 1

MNG_DELTATYPE_REPLACERGB         = 0       # PPLT
MNG_DELTATYPE_DELTARGB           = 1
MNG_DELTATYPE_REPLACEALPHA       = 2
MNG_DELTATYPE_DELTAALPHA         = 3
MNG_DELTATYPE_REPLACERGBA        = 4
MNG_DELTATYPE_DELTARGBA          = 5

MNG_POLARITY_ONLY                = 0       # DBYK
MNG_POLARITY_ALLBUT              = 1

MNG_EVENT_NONE                   = 0       # evNT
MNG_EVENT_MOUSEENTER             = 1
MNG_EVENT_MOUSEMOVE              = 2
MNG_EVENT_MOUSEEXIT              = 3
MNG_EVENT_MOUSEDOWN              = 4
MNG_EVENT_MOUSEUP                = 5

MNG_MASK_NONE                    = 0       # evNT
MNG_MASK_BOX                     = 1
MNG_MASK_OBJECT                  = 2
MNG_MASK_OBJECTIX                = 3
MNG_MASK_BOXOBJECT               = 4
MNG_MASK_BOXOBJECTIX             = 5

# **************************************************************************
# *                                                                        *
# *  Processtext callback types                                            *
# *                                                                        *
# **************************************************************************

MNG_TYPE_TEXT = 0
MNG_TYPE_ZTXT = 1
MNG_TYPE_ITXT = 2

# **************************************************************************
# *                                                                        *
# *  CRC processing masks                                                  *
# *                                                                        *
# **************************************************************************

MNG_CRC_INPUT              = 0x0000000f
MNG_CRC_INPUT_NONE         = 0x00000000
MNG_CRC_INPUT_PRESENT      = 0x00000001
MNG_CRC_OUTPUT             = 0x000000f0
MNG_CRC_OUTPUT_NONE        = 0x00000000
MNG_CRC_OUTPUT_GENERATE    = 0x00000020
MNG_CRC_OUTPUT_DUMMY       = 0x00000040
MNG_CRC_ANCILLARY          = 0x00000f00
MNG_CRC_ANCILLARY_IGNORE   = 0x00000000
MNG_CRC_ANCILLARY_DISCARD  = 0x00000100
MNG_CRC_ANCILLARY_WARNING  = 0x00000200
MNG_CRC_ANCILLARY_ERROR    = 0x00000300
MNG_CRC_CRITICAL           = 0x0000f000
MNG_CRC_CRITICAL_IGNORE    = 0x00000000
MNG_CRC_CRITICAL_WARNING   = 0x00002000
MNG_CRC_CRITICAL_ERROR     = 0x00003000
MNG_CRC_DEFAULT            = 0x00002121

