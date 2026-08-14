#Requires AutoHotkey v2.0
#SingleInstance Force

running := false
printing := false


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
    global running, printing

    running := false
    printing := false

    SetTimer SAPAutomation, 0

    ToolTip "STOPPED"
    SetTimer RemoveToolTip, -1200
}


; =========================================================
; MAIN AUTOMATION
; =========================================================

SAPAutomation() {

    global running, printing

    if !running
        return


    ; =====================================================
    ; 1. CHECK FOR PDF ERROR WINDOW
    ; =====================================================

    dialogs := WinGetList("ahk_class #32770")

    for hwnd in dialogs {

        try {
            title := WinGetTitle("ahk_id " hwnd)
            text := WinGetText("ahk_id " hwnd)

            if InStr(text, "This file does not have an app associated with it") {

                ; Activate the error dialog
                WinActivate "ahk_id " hwnd

                Sleep 100

                ; ENTER = OK
                Send "{Enter}"

                Sleep 500

                printing := false

                return
            }
        }
    }


    ; =====================================================
    ; 2. FIND SAP PRINT WINDOW
    ; =====================================================

    printWindows := WinGetList("ahk_class #32770")

    for hwnd in printWindows {

        try {

            title := WinGetTitle("ahk_id " hwnd)


            ; Only work with SAP's "Print:" window
            if InStr(title, "Print:") {

                ; Don't repeatedly click the same Print window
                if printing
                    return

                printing := true


                ; =================================================
                ; CLICK SAP PRINT BUTTON
                ;
                ; Window Spy identified it as Button3
                ; =================================================

                ControlClick(
                    "Button3",
                    "ahk_id " hwnd,
                    ,
                    "Left",
                    1,
                    "NA"
                )

                ; Give SAP time to process the print
                Sleep 1000

                return
            }
        }
    }
}


; =========================================================
; REMOVE TOOLTIP
; =========================================================

RemoveToolTip() {
    ToolTip
}