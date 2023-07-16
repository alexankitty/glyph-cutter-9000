import PySimpleGUI as sg
import sys
import imageProcessor
import strings
import random
def run():
    file_list_column = [
        [
            sg.Text('Required Fields'),
            sg.HSep(color=None, pad=None)
        ],
        [
            sg.Text("Tip: For additional information, however over the text next to the input box.")
        ],
        [
            sg.Text("Bitmap Image:",size=(19,1), tooltip=strings.imageFileHelp),
            sg.In(size=(20, 1), key="imageFile"),
            sg.FileBrowse(button_text="Browse",file_types = (('Image Files', '.bmp .png .jpg .jpeg'),))
        ],
        [
            sg.Text("Output File:",size=(19,1), tooltip=strings.outputFileHelp),
            sg.In(size=(20, 1), key="outputFile"),
            sg.FileSaveAs()
        ],
        [
            sg.Text("Kerning Size (px):",size=(19,1), tooltip=strings.kerningSizeHelp),
            sg.In(size=(20, 1), key="kerningSize")
        ],
        [
            sg.Text("Glyph Size (px):",size=(19,1), tooltip=strings.glyphSizeHelp),
            sg.In(size=(20, 1), key="glyphSize")
        ],
        [
            sg.Text('Optional fields'),
            sg.HSep(color=None, pad=None)
        ],
        [
            sg.Text("Glyph Limit:", size=(19,1), tooltip=strings.glyphLimitHelp),
            sg.In(size=(20,1), key="glyphLimit")
        ],
        [
            sg.Text("Template File:",size=(19,1), tooltip=strings.templateFileHelp),
            sg.In(size=(20,1), key="templateFile"),
            sg.FileBrowse(button_text="Browse")
        ],
        [
            sg.Text("Matching pixel count (px):",size=(19,1), tooltip=strings.matchPxHelp),
            sg.In(size=(20, 1), key="matchPX")
        ],
        [
            sg.Text("Color Threshold:",size=(19,1), tooltip=strings.colorThresholdHelp),
            sg.In(size=(20, 1), key="colorThreshold")
        ],
                [
            sg.Text("Top offset (px):",size=(19,1), tooltip=strings.topOffsetHelp),
            sg.In(size=(20, 1),key="topOffset")
        ],
        [
            sg.Text("Bottom offset (px):",size=(19,1), tooltip=strings.bottomOffsetHelp),
            sg.In(size=(20, 1), key="bottomOffset")
        ],
        [
            sg.Text("Space size (px):",size=(19,1), tooltip=strings.spaceSizeHelp),
            sg.In(size=(20, 1), key="spaceSize")
        ],   
        [
            sg.Text("Space coordinates (x,y):",size=(19,1), tooltip=strings.spaceCoordHelp),
            sg.In(size=(20, 1), key="spaceCoord")
        ],   
        [
            sg.Text("Empty Glyph Size (px):",size=(19,1), tooltip=strings.glyphSizeHelp),
            sg.In(size=(20, 1), key="emptySize")
        ],
        [
            sg.Checkbox('Left-side Kerning', key="leftKerning", tooltip=strings.leftKerningHelp)
        ],
        [
            sg.Checkbox('Right-side Kerning', key="rightKerning", tooltip=strings.rightKerningHelp)
        ],
        [
            sg.Checkbox('Treat Solid Glyph As End', key="solidBehavior", tooltip=strings.solidBehaviorHelp)
        ],
        [
            sg.Checkbox('Retry On Cut Failure', key="retry", tooltip=strings.retryHelp)
        ],
        [
            sg.Button('Cut Fonts!', enable_events=True, key='-CUTFONTS-')
        ]
    ]
    console_output_column = [
        [
            sg.Output(size=(60,30))
        ]
    ]
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(console_output_column),
        ]
    ]
    window = sg.Window("Glyph Cutter 9000", layout)
    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        # Image selected, display it.
        
        if event == "-CUTFONTS-":
            cutFonts(values) 
    window.close()
    sys.exit()
    
def cutFonts(values):
    try:
        imageFile = values['imageFile']
        outputFile = values['outputFile']
        kerningSize = int(values['kerningSize'])
        glyphSize = int(values['glyphSize'])
        templateFile = values['templateFile']
        leftKerning = values['leftKerning']
        rightKerning = values['rightKerning']
        solidBehavior = values['solidBehavior']
        spaceCoord = values['spaceCoord']
        if not templateFile:
            templateFile = None
        if not leftKerning:
            leftKerning = None
        if not rightKerning:
            rightKerning = None
        if not solidBehavior:
            solidBehavior = None
        matchPX = None if not values['matchPX'] else int(values['matchPX'])
        colorThreshold = None if not values['colorThreshold'] else int(values['colorThreshold'])
        topOffset = None if not values['topOffset'] else int(values['topOffset'])
        bottomOffset = None if not values['bottomOffset'] else int(values['bottomOffset'])
        spaceSize = None if not values['spaceSize'] else int(values['spaceSize'])
        emptySize = None if not values['emptySize'] else int(values['emptySize']) 
        glyphLimit = None if not values['glyphLimit'] else int(values['glyphLimit'])
        retry = values['retry']
        if not spaceCoord:
            spaceCoord = None
    except Exception:
        sg.popup_error("Parameter failure, a size could not be converted to integer.")
        return
    #if not imageFile or not outputFile or not kerningSize or not glyphSize:
    if not imageFile or not outputFile or kerningSize == "" or glyphSize == "":
        sg.popup_error("Missing a required field.")
        return
    try:
        font = imageProcessor.Font(imageFile, glyphSize, kerningSize, emptySize, spaceSize, spaceCoord, solidBehavior, leftKerning, rightKerning, matchPX, topOffset, bottomOffset, colorThreshold, glyphLimit, retry, templateFile)
        cuts = font.cutGlyphs()
        process = font.processCuts()
        output = open(outputFile, 'w')
        output.write(process)
    except Exception as e:
        sg.popup_error_with_traceback(str(e))
    if not round(random.random() * 100) == 69:
        print("Finished cutting fonts. Thank you and have a wonderful day.")
    else:
        print("Finished cutting fonts, now get the hell off my property.")