#Requires AutoHotkey v2.0
#SingleInstance Force

running := false

; How often to check SAP
checkDelay := 300


; =========================================================
; F6 = START / STOP
; =========================================================

F6:: {
    global running

    running := !running

    if running {
        SetTimer SAPAutomation, 300

        ToolTip "SAP AUTO PRINT: ON"
        SetTimer RemoveToolTip, -1200
    }
    else {
        SetTimer SAPAutomation, 0

        ToolTip "SAP AUTO PRINT: OFF"
        SetTimer RemoveToolTip, -1200
    }
}


; =========================================================
; F7 = EMERGENCY STOP
; =========================================================

F7:: {
    global running

    running := false
    SetTimer SAPAutomation, 0

    ToolTip "STOPPED"
    SetTimer RemoveToolTip, -1200
}


; =========================================================
; MAIN AUTOMATION
; =========================================================

SAPAutomation() {

    global running

    if !running
        return


    ; -----------------------------------------------------
    ; 1. CHECK FOR WINDOWS PDF ERROR
    ; -----------------------------------------------------

    dialogs := WinGetList("ahk_class #32770")

    for hwnd in dialogs {

        try {
            text := WinGetText("ahk_id " hwnd)

            if InStr(text, "This file does not have an app associated with it") {

                ; Activate the error dialog
                WinActivate "ahk_id " hwnd

                Sleep 100

                ; Click/press OK
                Send "{Enter}"

                Sleep 300

                return
            }
        }
    }


    ; -----------------------------------------------------
    ; 2. CHECK FOR SAP PRINT WINDOW
    ; -----------------------------------------------------

    printWindows := WinGetList("Print:")

    for hwnd in printWindows {

        try {

            ; Get window position
            WinGetPos &wx, &wy, &ww, &wh, "ahk_id " hwnd

            ; Print button is approximately at the
            ; bottom-right of the SAP Print window.
            ;
            ; We use ControlClick with coordinates
            ; relative to the window.
            ;
            ; This does NOT intentionally move your mouse.

            printX := ww - 75
            printY := wh - 35

            ControlClick(
                "x" printX " y" printY,
                "ahk_id " hwnd,
                ,
                "Left",
                1,
                "NA"
            )

            Sleep 500

            return
        }
    }
}


; =========================================================
; REMOVE TOOLTIP
; =========================================================

RemoveToolTip() {
    ToolTip
}