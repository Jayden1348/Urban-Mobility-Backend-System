; AutoHotkey v2 code
; Press Numpad1 to paste example multi-line text

Numpad1::{
	Send "1"
	Send "{Enter}"
	SendText "engineer1"
	Send "{Enter}"
	SendText "EngPass1!"
	Send "{Enter}"
}

Numpad2::{
	Send "1"
	Send "{Enter}"
	SendText "sysadmin1"
	Send "{Enter}"
	SendText "SysPass1!"
	Send "{Enter}"
}

Numpad3::{
	Send "1"
	Send "{Enter}"
	SendText "super_admin"
	Send "{Enter}"
	SendText "Admin_123?"
	Send "{Enter}"
}
