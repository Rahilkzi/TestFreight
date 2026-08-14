#Requires AutoHotkey v2.0
#SingleInstance Force

running := false
printClicked := false


; =========================================================
; F6 = START / STOP
; =========================================================

F6:: {
    global running

    running := !running

    if running {
        SetTimer SAPAutomation, 200

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
    global running, printClicked

    running := false
    printClicked := false

    SetTimer SAPAutomation, 0

    ToolTip "STOPPED"
    SetTimer RemoveToolTip, -1200
}


; =========================================================
; MAIN AUTOMATION
; =========================================================

SAPAutomation() {

    global running, printClicked

    if !running
        return


    ; =====================================================
    ; STEP 1 — LOOK FOR ERROR WINDOW
    ; =====================================================

    dialogs := WinGetList("ahk_class #32770")

    errorFound := false

    for hwnd in dialogs {

        try {
            text := WinGetText("ahk_id " hwnd)

            if InStr(text, "This file does not have an app associated with it") {

                errorFound := true

                ; Bring error window forward
                WinActivate "ahk_id " hwnd

                Sleep 100

                ; ENTER = OK
                Send "{Enter}"

                Sleep 500

                ; Ready for next print
                printClicked := false

                return
            }
        }
    }


    ; =====================================================
    ; STEP 2 — IF NO ERROR, LOOK FOR SAP PRINT WINDOW
    ; =====================================================

    if !errorFound {

        printWindows := WinGetList("ahk_class #32770")

        for hwnd in printWindows {

            try {
                title := WinGetTitle("ahk_id " hwnd)

                ; SAP Print window
                if InStr(title, "Print:") {

                    ; Prevent repeated clicking
                    if printClicked
                        return

                    printClicked := true

                    ; Button3 = PRINT
                    ControlClick(
                        "Button3",
                        "ahk_id " hwnd,
                        ,
                        "Left",
                        1,
                        "NA"
                    )

                    Sleep 1000

                    return
                }
            }
        }
    }


    ; =====================================================
    ; STEP 3 — NO PRINT WINDOW = READY FOR NEXT ONE
    ; =====================================================

    printWindows := WinGetList("ahk_class #32770")

    hasPrintWindow := false

    for hwnd in printWindows {
        try {
            title := WinGetTitle("ahk_id " hwnd)

            if InStr(title, "Print:") {
                hasPrintWindow := true
                break
            }
        }
    }

    if !hasPrintWindow {
        printClicked := false
    }
}


; =========================================================
; REMOVE TOOLTIP
; =========================================================

RemoveToolTip() {
    ToolTip
}