#Requires AutoHotkey v2.0

running := false
clickX := 0
clickY := 0
clickDelay := 500


; F8 = Save the button position
F8:: {
    global clickX, clickY

    MouseGetPos &clickX, &clickY

    ToolTip "Button position saved:`n" clickX ", " clickY
    SetTimer RemoveToolTip, -1500
}


; F6 = Start / Stop
F6:: {
    global running

    running := !running

    if running {
        SetTimer AutoClick, 500
        SetTimer CheckError, 200

        ToolTip "AUTO CLICK: ON"
    }
    else {
        SetTimer AutoClick, 0
        SetTimer CheckError, 0

        ToolTip "AUTO CLICK: OFF"
    }

    SetTimer RemoveToolTip, -1000
}


; F7 = Emergency stop
F7:: {
    global running

    running := false
    SetTimer AutoClick, 0
    SetTimer CheckError, 0

    ToolTip "STOPPED"
    SetTimer RemoveToolTip, -1000
}


; Automatic click
AutoClick() {
    global clickX, clickY

    ; Remember where your cursor currently is
    MouseGetPos &oldX, &oldY

    ; Click the target
    Click clickX, clickY

    ; Put cursor back where it was
    MouseMove oldX, oldY, 0
}


; Detect the Windows error
CheckError() {

    dialogs := WinGetList("ahk_class #32770")

    for hwnd in dialogs {
        try {
            text := WinGetText(hwnd)

            if InStr(text, "This file does not have an app associated with it") {
                WinActivate hwnd
                Sleep 100
                Send "{Enter}"
                return
            }
        }
    }
}


RemoveToolTip() {
    ToolTip
}