#Requires AutoHotkey v2.0
#SingleInstance Force

; ============================================================
; SETTINGS
; ============================================================

; Your application's executable
appExe := "YourApplication.exe"

; The control you want to repeatedly click.
; Example: "Button1"
targetControl := "Button1"

; Time between clicks in milliseconds
clickDelay := 500

; ============================================================
; STATE
; ============================================================

running := false


; ============================================================
; F6 = START / STOP
; ============================================================

F6:: {
    global running, clickDelay

    running := !running

    if running {
        SetTimer AutoClick, clickDelay
        SetTimer CheckError, 200

        ToolTip "AUTO CLICK: ON"
        SetTimer RemoveToolTip, -1000
    }
    else {
        SetTimer AutoClick, 0
        SetTimer CheckError, 0

        ToolTip "AUTO CLICK: OFF"
        SetTimer RemoveToolTip, -1000
    }
}


; ============================================================
; F7 = EMERGENCY STOP
; ============================================================

F7:: {
    global running

    running := false

    SetTimer AutoClick, 0
    SetTimer CheckError, 0

    ToolTip "STOPPED"
    SetTimer RemoveToolTip, -1000
}


; ============================================================
; AUTOMATIC CLICK
; ============================================================

AutoClick() {
    global appExe, targetControl

    ; Find your application
    hwnd := WinExist("ahk_exe " appExe)

    if !hwnd
        return

    ; Send click directly to the Windows control.
    ; The physical mouse does NOT move.
    try {
        ControlClick targetControl, "ahk_id " hwnd
    }
}


; ============================================================
; CHECK FOR YOUR WINDOWS ERROR
; ============================================================

CheckError() {

    ; Windows standard dialog
    dialogs := WinGetList("ahk_class #32770")

    for hwnd in dialogs {

        try {
            text := WinGetText(hwnd)

            ; Detect the error from your screenshot
            if InStr(text, "This file does not have an app associated with it") {

                ; Activate error window
                WinActivate "ahk_id " hwnd

                Sleep 100

                ; Press OK
                Send "{Enter}"

                return
            }
        }
    }
}


; ============================================================
; REMOVE TOOLTIP
; ============================================================

RemoveToolTip() {
    ToolTip
}


; ============================================================
; F8 = SHOW CURRENT APPLICATION INFORMATION
; ============================================================

F8:: {

    MouseGetPos , , &mouseHwnd

    try {
        title := WinGetTitle("ahk_id " mouseHwnd)
        exe := WinGetProcessName("ahk_id " mouseHwnd)
        class := WinGetClass("ahk_id " mouseHwnd)

        MsgBox(
            "Window information:`n`n"
            . "Title: " title "`n"
            . "EXE: " exe "`n"
            . "Class: " class
        )
    }
}