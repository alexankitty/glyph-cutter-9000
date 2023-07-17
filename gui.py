import PySimpleGUI as sg
import contextlib
import sys
import imageProcessor
import strings
import random
import regex
import contextlib

def run():
    def validate(text):
        result = regex.match(regexSearch, text)
        return result is not None and result.group() == text

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
            sg.FileSaveAs(file_types = (('Text Files','*.*'),))
        ],
        [
            sg.Text("Kerning Size (px):",size=(19,1), enable_events=True, tooltip=strings.kerningSizeHelp),
            sg.In(size=(20, 1), key="kerningSize")
        ],
        [
            sg.Text("Glyph Size (px):",size=(19,1), enable_events=True, tooltip=strings.glyphSizeHelp),
            sg.In(size=(20, 1), key="glyphSize")
        ],
        [
            sg.Text('Optional fields'),
            sg.HSep(color=None, pad=None)
        ],
        [
            sg.Text("Glyph Limit:", size=(19,1), enable_events=True, tooltip=strings.glyphLimitHelp),
            sg.In(size=(20,1), key="glyphLimit")
        ],
        [
            sg.Text("Template File:",size=(19,1), tooltip=strings.templateFileHelp),
            sg.In(size=(20,1), key="templateFile"),
            sg.FileBrowse(button_text="Browse")
        ],
        [
            sg.Text("Matching pixel count (px):",size=(19,1), enable_events=True, tooltip=strings.matchPxHelp),
            sg.In(size=(20, 1), key="matchPX")
        ],
        [
            sg.Text("Color Threshold:",size=(19,1), enable_events=True, tooltip=strings.colorThresholdHelp),
            sg.In(size=(20, 1), key="colorThreshold")
        ],
                [
            sg.Text("Top offset (px):",size=(19,1), enable_events=True, tooltip=strings.topOffsetHelp),
            sg.In(size=(20, 1),key="topOffset")
        ],
        [
            sg.Text("Bottom offset (px):",size=(19,1), enable_events=True, tooltip=strings.bottomOffsetHelp),
            sg.In(size=(20, 1), key="bottomOffset")
        ],
        [
            sg.Text("Space size (px):",size=(19,1), enable_events=True, tooltip=strings.spaceSizeHelp),
            sg.In(size=(20, 1), key="spaceSize")
        ],   
        [
            sg.Text("Space coordinates (x,y):",size=(19,1), tooltip=strings.spaceCoordHelp),
            sg.In(size=(20, 1), key="spaceCoord")
        ],   
        [
            sg.Text("Empty Glyph Size (px):",size=(19,1), enable_events=True, tooltip=strings.emptySizeHelp),
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
    window = sg.Window("Glyph Cutter 9000", layout, finalize=True)
    regexSearch = "^[+-]?([0-9]((\d*))?)?$"
    old = {'kerningSize':'',
        'glyphSize':'',
        'matchPX':'',
        'colorThreshold':'',
        'topOffset':'',
        'bottomOFfset':'',
        'spaceSize:':'',
        'emptySize':'',
        'glyphLimit':''
        }
    validate_inputs = ('kerningSize', 'glyphSize', 'matchPX', 'colorThreshold','topOffset','bottomOffset','spaceSize', 'emptySize','glyphLimit')
    for key in validate_inputs:
        window[key].bind('<Key>', ' KEY')

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break
        elif event == "-CUTFONTS-":
            cutFonts(values)
        elif event.endswith(' KEY'):
            key = event.split()[0]
            element, text = window[key], values[key]
            if validate(text):
                with contextlib.suppress(ValueError):
                    if not text:
                        element.update(text)
                        old[key] = text
                        continue
                    v = int(text)
                    element.update(v)
                    old[key] = v
                    continue
            else:
                print(f'Integers in {key} only.')
                element.update(old[key])
    window.close()
    sys.exit()
    
def cutFonts(values):
    imageFile = values['imageFile'] or None
    outputFile = values['outputFile'] or None
    kerningSize = None if values['kerningSize'] == '' else int(values['kerningSize'])
    glyphSize = None if values['glyphSize'] == '' else int(values['glyphSize'])
    templateFile = values['templateFile'] or None
    spaceCoord = values['spaceCoord'] or None
    matchPX = None if values['matchPX'] == '' else int(values['matchPX'])
    colorThreshold = None if values['colorThreshold'] == '' else int(values['colorThreshold'])
    topOffset = None if values['topOffset'] == '' else int(values['topOffset'])
    bottomOffset = None if values['bottomOffset'] == '' else int(values['bottomOffset'])
    spaceSize = None if values['spaceSize'] == '' else int(values['spaceSize'])
    emptySize = None if values['emptySize'] == '' else int(values['emptySize']) 
    glyphLimit = None if values['glyphLimit'] == '' else int(values['glyphLimit'])
    retry = values['retry']
    leftKerning = values['leftKerning']
    rightKerning = values['rightKerning']
    solidBehavior = values['solidBehavior']
    #if not imageFile or not outputFile or not kerningSize or not glyphSize:
    if None in (imageFile, outputFile, kerningSize, glyphSize):
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
    if round(random.random() * 100) != 69:
        print("Finished cutting fonts. Thank you and have a wonderful day.")
    else:
        print("Finished cutting fonts, now get the hell off my property.")