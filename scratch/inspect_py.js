Process.enumerateModules().forEach(m => {
    if (m.name.includes("client") || m.name.includes("neox") || m.name.includes("python") || m.name.includes("game")) {
        console.log("Module:", m.name, "Base:", m.base, "Path:", m.path);
    }
});

