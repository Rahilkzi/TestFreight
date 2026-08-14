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
        SetTimer SAPAutomation, 200
        ToolTip "AUTO PRINT: ON"
    }
    else {
        SetTimer SAPAutomation, 0
        ToolTip "AUTO PRINT: OFF"
    }

    SetTimer RemoveToolTip, -1000
}


; =========================================================
; F7 = STOP
; =========================================================

F7:: {
    global running

    running := false
    SetTimer SAPAutomation, 0

    ToolTip "STOPPED"
    SetTimer RemoveToolTip, -1000
}


; =========================================================
; MAIN LOOP
; =========================================================

SAPAutomation() {

    global running

    if !running
        return


    ; ---------------------------------------------------------
    ; FIRST: Is the ERROR window showing?
    ; ---------------------------------------------------------

    windows := WinGetList("ahk_class #32770")

    for hwnd in windows {

        try {
            text := WinGetText("ahk_id " hwnd)

            if InStr(text, "This file does not have an app associated with it") {

                WinActivate "ahk_id " hwnd

                Sleep 100

                ; ONLY NOW press Enter
                Send "{Enter}"

                Sleep 500

                return
            }
        }
    }


    ; ---------------------------------------------------------
    ; SECOND: Is SAP PRINT window showing?
    ; ---------------------------------------------------------

    windows := WinGetList("ahk_class #32770")

    for hwnd in windows {

        try {
            title := WinGetTitle("ahk_id " hwnd)

            if InStr(title, "Print:") {

                ; Button3 = Print
                ControlClick(
                    "Button3",
                    "ahk_id " hwnd,
                    ,
                    "Left",
                    1,
                    "NA"
                )

                ; Wait before checking again
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