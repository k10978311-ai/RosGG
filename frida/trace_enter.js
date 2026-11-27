/**
 * READ-ONLY RE trace of the entity "enter world" path (observes only).
 *   0x91d214 ClientApp::onEntityEnter(this, id, spaceID, vehicleID)
 *   0x926f9c Entity prerequisites gate (Python prerequisites() == True)  -> return value
 *   0x91d5f4 replay of buffered entity messages (+0x1088)
 *   0x931494 Player::setPlayer(player, entity)
 *   0x91cd04 ClientApp::onCellPlayerCreate
 *   0x91e960 ClientApp::onEntityMethod(this, id, idx, stream)
 *   0x9260d0 Entity::onMethod (dispatched!)
 * LDPlayer: python run_frida.py frida/trace_enter.js --attach --realm emulated
 */
const lib = Process.findModuleByName("libclient.so");
const B = (o) => lib.base.add(o);
function hook(off, name, onEnter, onLeave) {
    try {
        Interceptor.attach(B(off), { onEnter: onEnter || function () { console.log("[" + name + "]"); }, onLeave: onLeave });
        console.log("[+] " + name);
    } catch (e) { console.log("[-] " + name + ": " + e); }
}
if (!lib) { console.log("[-] libclient.so not found"); } else {
    hook(0x91d214, "onEntityEnter", function (a) { console.log("[onEntityEnter] id=" + a[1].toInt32() + " space=" + a[2].toInt32() + " vehicle=" + a[3].toInt32()); });
    hook(0x926f9c, "prerequisites", function (a) { this.e = a[0]; }, function (r) { console.log("[prerequisites] entity=" + this.e + " -> " + r.toInt32()); });
    hook(0x91d5f4, "replayBuffered", function (a) { console.log("[replayBuffered] entity=" + a[1]); });
    hook(0x931494, "Player::setPlayer", function (a) { console.log("[setPlayer] entity=" + a[1]); });
    hook(0x91cd04, "onCellPlayerCreate");
    hook(0x91e960, "onEntityMethod", function (a) { console.log("[onEntityMethod] id=" + a[1].toInt32() + " idx=" + a[2].toInt32()); });
    hook(0x9260d0, "Entity::onMethod", function (a) { console.log("[Entity::onMethod] DISPATCHED idx=" + a[1].toInt32()); });
}
