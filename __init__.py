#Requires AutoHotkey v2.0
#SingleInstance Force

running := false


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
; MAIN SAP AUTOMATION
; =========================================================

SAPAutomation() {

    global running

    if !running
        return


    ; =====================================================
    ; 1. CHECK FOR WINDOWS PDF ERROR
    ; =====================================================

    dialogs := WinGetList("ahk_class #32770")

    for hwnd in dialogs {

        try {
            text := WinGetText("ahk_id " hwnd)

            if InStr(text, "This file does not have an app associated with it") {

                ; Activate the error dialog
                WinActivate "ahk_id " hwnd

                Sleep 100

                ; Press ENTER = OK
                Send "{Enter}"

                Sleep 500

                return
            }
        }
    }


    ; =====================================================
    ; 2. FIND SAP PRINT WINDOW
    ; =====================================================

    printWindows := WinGetList("Print:")

    for hwnd in printWindows {

        try {

            ; Get SAP Print window position and size
            WinGetPos &wx, &wy, &ww, &wh, "ahk_id " hwnd


            ; ------------------------------------------------
            ; PRINT BUTTON
            ;
            ; Based on your SAP Print window screenshot.
            ; ------------------------------------------------

            clickX := wx + ww - 75
            clickY := wy + wh - 25


            ; Save current mouse position
            MouseGetPos &oldX, &oldY


            ; Activate SAP Print window
            WinActivate "ahk_id " hwnd

            Sleep 100


            ; Move to Print button
            MouseMove clickX, clickY, 0


            ; REAL LEFT CLICK
            Click "Left"


            ; Small delay
            Sleep 100


            ; Return mouse to original position
            MouseMove oldX, oldY, 0


            ; Give SAP time to process
            Sleep 800

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