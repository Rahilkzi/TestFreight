#Requires AutoHotkey v2.0

running := false
clickX := 0
clickY := 0

; Change this if you want faster/slower clicking
clickDelay := 500


; =====================================
; F8 = SAVE MOUSE POSITION
; =====================================

F8:: {
    global clickX, clickY

    MouseGetPos &clickX, &clickY

    ToolTip "Position saved: " clickX ", " clickY
    SetTimer RemoveToolTip, -1500
}


; =====================================
; F6 = START / STOP
; =====================================

F6:: {
    global running, clickX, clickY, clickDelay

    if (clickX = 0 && clickY = 0) {
        MsgBox "First move the mouse over the button and press F8."
        return
    }

    running := !running

    if running {
        SetTimer DoClick, clickDelay
        SetTimer CheckError, 100

        ToolTip "AUTO CLICK ON"
    }
    else {
        SetTimer DoClick, 0
        SetTimer CheckError, 0

        ToolTip "AUTO CLICK OFF"
    }

    SetTimer RemoveToolTip, -1000
}


; =====================================
; F7 = EMERGENCY STOP
; =====================================

F7:: {
    global running

    running := false

    SetTimer DoClick, 0
    SetTimer CheckError, 0

    ToolTip "STOPPED"
    SetTimer RemoveToolTip, -1000
}


; =====================================
; PERFORM CLICK
; =====================================

DoClick() {
    global clickX, clickY

    Click clickX, clickY
}


; =====================================
; CHECK FOR WINDOWS ERROR DIALOG
; =====================================

CheckError() {

    ; Standard Windows dialog
    dialogs := WinGetList("ahk_class #32770")

    for hwnd in dialogs {

        try {
            text := WinGetText(hwnd)

            if InStr(text, "This file does not have an app associated with it") {

                WinActivate hwnd
                Sleep 100

                ; Press OK
                Send "{Enter}"

                return
            }
        }
    }
}


; =====================================
; REMOVE TOOLTIP
; =====================================

RemoveToolTip() {
    ToolTip
}