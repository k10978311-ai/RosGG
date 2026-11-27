with open(OUT, 'w') as f:
    try:
        import BigWorld
        p = BigWorld.player()
        f.write('Calling tryUploadRCVersion...\n')
        p.tryUploadRCVersion()
        f.write('tryUploadRCVersion succeeded!\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
