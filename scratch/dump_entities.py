import frida, sys, time

device = frida.get_device_manager().get_device('emulator-5554')
session = device.attach('com.netease.chiji', realm='emulated')

js_code = """
const libclient = Process.findModuleByName('libclient.so');
if (libclient) {
    const base = libclient.base;
    const vec_addr = base.add(0x44db0e8);
    const p_begin = vec_addr.readPointer();
    const p_end = vec_addr.add(8).readPointer();
    const count = p_end.sub(p_begin).toInt32() / 8;
    
    let res = [];
    for (let i = 0; i < count; i++) {
        const pEntityType = p_begin.add(i * 8).readPointer();
        if (pEntityType.isNull()) {
            res.push({i: i, typeIndex: 0, name: 'NULL'});
            continue;
        }
        const typeIndex = pEntityType.readU32();
        
        // libc++ std::string at offset 8
        const str_base = pEntityType.add(8);
        const b0 = str_base.readU8();
        let name = '';
        if ((b0 & 1) === 0) {
            const len = b0 >> 1;
            if (len > 0) {
                name = str_base.add(1).readUtf8String(len);
            }
        } else {
            const len = str_base.add(8).readU64().toInt32();
            const data_ptr = str_base.add(16).readPointer();
            if (!data_ptr.isNull() && len > 0 && len < 200) {
                name = data_ptr.readUtf8String(len);
            }
        }
        res.push({i: i, typeIndex: typeIndex, name: name});
    }
    send(res);
}
"""

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        print(f"Total entity types loaded: {len(payload)}")
        for item in payload:
            n = item['name']
            if any(k in n for k in ['Avatar', 'Account', 'Login', 'Player', 'Hall']) or item['i'] < 10:
                print(f"  [{item['i']:3}] typeIndex={item['typeIndex']:3} name='{n}'")
    else:
        print(message)

script = session.create_script(js_code)
script.on('message', on_message)
script.load()
time.sleep(1)
session.detach()
