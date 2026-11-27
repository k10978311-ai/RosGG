import Globals, traceback

f = open(OUT, 'w')
try:
    uiMgr = Globals.uiMgr
    all_ui = getattr(uiMgr, '____all_ui__', {})
    
    # 1. Leave Facebook UI
    try:
        uiMgr.leave_ui('UIFollowonFacebook')
        f.write("[+] leave_ui UIFollowonFacebook success\n")
    except Exception as e:
        f.write("[-] leave_ui UIFollowonFacebook: %s\n" % e)
        
    fb_ui = all_ui.get('UIFollowonFacebook')
    if fb_ui and hasattr(fb_ui, 'panel'):
        fb_ui.panel.setVisible(False)
        f.write("[+] UIFollowonFacebook panel setVisible(False)\n")

    # 2. Hide QR Code and PC Login in UILogin
    uilogin = all_ui.get('UILogin')
    if uilogin:
        # qrcode
        if hasattr(uilogin, 'qrcodeImg') and uilogin.qrcodeImg:
            uilogin.qrcodeImg.setVisible(False)
            f.write("[+] uilogin.qrcodeImg setVisible(False)\n")
        
        # UserScan / QR scan button
        if hasattr(uilogin, 'uiQRScan') and uilogin.uiQRScan:
            uilogin.uiQRScan.setVisible(False)
            f.write("[+] uilogin.uiQRScan setVisible(False)\n")
            
        # Also check panel widgets
        if hasattr(uilogin, 'panel'):
            for p in ['LeftUpAnchor/UserScan', 'RightUpAnchor/UserScan', 'qrcode_img', 'img_qrcode', 'qrcode', 'MiddleAnchor/qrcode']:
                try:
                    w = uilogin.panel.get_widget_by_path(p)
                    if w:
                        w.setVisible(False)
                        f.write("[+] uilogin widget %s setVisible(False)\n" % p)
                except:
                    pass

    # 3. Check UILanguageBtn
    ulang = all_ui.get('UILanguageBtn')
    if ulang and hasattr(ulang, 'panel'):
        for p in ['top_right/btn_scan', 'btn_scan']:
            try:
                w = ulang.panel.get_widget_by_path(p)
                if w:
                    w.setVisible(False)
                    f.write("[+] UILanguageBtn widget %s setVisible(False)\n" % p)
            except:
                pass

except Exception:
    f.write(traceback.format_exc())
f.close()
