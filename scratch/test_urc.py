with open(OUT, 'w') as f:
    import BigWorld
    p = BigWorld.player()
    f.write('has uploadRCVersion: ' + repr(hasattr(p.base, 'uploadRCVersion')) + '\n')
    if hasattr(p.base, 'uploadRCVersion'):
        f.write('uploadRCVersion: ' + repr(p.base.uploadRCVersion) + '\n')
