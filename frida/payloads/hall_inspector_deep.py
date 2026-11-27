# READ-ONLY: Comprehensive Deep Hall & Athlete State Inspector
import sys, traceback, types

f = open(OUT, 'w')
def w(s): f.write(str(s) + '\n')

w("=== DEEP HALL GAME INSPECTOR ===")
try:
    import BigWorld, Globals, ClientEntity
    
    # 1. BigWorld Global State
    w("\n--- [BigWorld State] ---")
    w("connectedAddress=%r" % (getattr(BigWorld, 'connectedAddress', lambda: '<na>')(),))
    w("spaceID=%r" % (getattr(BigWorld, 'spaceID', lambda: '<na>')(),))
    w("time=%r" % (getattr(BigWorld, 'time', lambda: '<na>')(),))
    w("prereqEntities=%r" % (getattr(BigWorld, 'prereqEntities', lambda: '<na>')(),))
    w("cachedEntities=%r" % (getattr(BigWorld, 'cachedEntities', lambda: '<na>')(),))
    
    entities = getattr(BigWorld, 'entities', {})
    w("entities count=%d" % len(entities))
    for eid, ent in dict(entities.items()).items():
        w("  Entity #%r class=%s position=%r" % (eid, ent.__class__.__name__, getattr(ent, 'position', None)))

    # 2. Player Entity
    w("\n--- [Player Entity] ---")
    p = BigWorld.player()
    w("BigWorld.player() = %r" % (p,))
    if p is not None:
        w("  class=%s module=%s id=%r" % (p.__class__.__name__, p.__class__.__module__, getattr(p, 'id', None)))
        w("  MRO=%s" % ([c.__name__ for c in p.__class__.__mro__[:8]],))
        
        # Identity / Core Base Properties
        core_attrs = [
            'id', 'playerUUID', 'playerName', 'identifierName', 'baseNickname', 'gid',
            'baseLevel', 'baseCharacterType', 'hostID', 'msHttpAP', 'isMobileAccount',
            'canCreateRoom', 'needNormalRoomTip', 'needOBRoomTip'
        ]
        w("  [Core Attributes]")
        for k in core_attrs:
            try:
                w("    %s = %r" % (k, getattr(p, k, '<missing>')))
            except Exception as e:
                w("    %s: ERR %r" % (k, e))
                
        # Currency & Economy
        econ_attrs = ['freeYuanbao', 'payYuanbao', 'currencyList', 'gold', 'diamond']
        w("  [Economy & Currency]")
        for k in econ_attrs:
            try:
                w("    %s = %r" % (k, getattr(p, k, '<missing>')))
            except Exception as e:
                w("    %s: ERR %r" % (k, e))

        # Appearance & Items
        appear_attrs = [
            'dtsAppearancePackage', 'dtsRos2DfdBattleItemPackage', 'currentGender',
            'showBodyAppearanceList', 'showWearableAppearanceList'
        ]
        w("  [Appearance & Packages]")
        for k in appear_attrs:
            try:
                val = getattr(p, k, '<missing>')
                if isinstance(val, (list, tuple, dict)) and len(val) > 20:
                    w("    %s = len %d: %r..." % (k, len(val), str(val)[:200]))
                else:
                    w("    %s = %r" % (k, val))
            except Exception as e:
                w("    %s: ERR %r" % (k, e))

        # Hall / Lobby specific attributes on player
        hall_attrs = [
            'isInHall', 'hallSceneReady', 'currentMapID', 'inLoading',
            'luckyCarnivalData', 'accumulateChargeData', 'monthPayRebateSpecialAwardInfo',
            'syncRedPoints', 'roleCreateTime', 'loginTime'
        ]
        w("  [Lobby State & Data]")
        for k in hall_attrs:
            try:
                w("    %s = %r" % (k, getattr(p, k, '<missing>')))
            except Exception as e:
                w("    %s: ERR %r" % (k, e))

    # 3. Application & Scene System
    w("\n--- [Application & Scene State] ---")
    App = vars(ClientEntity).get('Application')
    w("Application = %r" % (App,))
    if App:
        for attr in ('scene', 'level', '____scene_object__', '____level_object__'):
            w("  Application.%s = %r" % (attr, getattr(App, attr, '<missing>')))

    # Globals module check
    w("\n--- [Globals State] ---")
    for k in [
        'player', 'isInHall', 'hallSceneReady', 'isInGame', 'MAP_ID',
        'inLoading', 'loginResReady', 'loginScene', 'serverSauthInfo',
        'curScene', 'gameInit', 'netProxy', 'loginProxy'
    ]:
        try:
            w("  Globals.%s = %r" % (k, getattr(Globals, k, '<missing>')))
        except Exception as e:
            w("  Globals.%s: ERR %r" % (k, e))

    # 4. UI Manager & Active UIs
    w("\n--- [UI Manager State] ---")
    um = getattr(Globals, 'uiMgr', None)
    w("Globals.uiMgr = %r" % (um,))
    if um:
        vis = getattr(um, '_UIMgr____all_ui__vis', None)
        if isinstance(vis, dict):
            visible_uis = {k: v for k, v in vis.items() if v}
            w("  Visible UIs (%d): %r" % (len(visible_uis), visible_uis))
        times = getattr(um, '_UIMgr____all_ui_enter_times', None)
        if isinstance(times, dict):
            recent_times = {k: v for k, v in times.items() if v}
            w("  Entered UIs (%d): %r" % (len(recent_times), recent_times))
        stack = getattr(um, '_UIMgr____ui_stack', None)
        if stack:
            w("  UI Stack: %r" % (stack,))

except Exception:
    w("UNCAUGHT EXCEPTION IN INSPECTOR:")
    w(traceback.format_exc())

w("\n=== END OF INSPECTION ===")
f.close()
