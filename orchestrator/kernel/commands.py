# -*- coding: utf-8 -*-
"""Comandos del usuario (/estado /conflictos /resolver /frontera /handoff)."""
def handle(texto, db, outputs):
    p = texto.strip().split()
    cmd = p[0].lower() if p else ""
    if cmd == "/estado":
        docs = len(db.inv_por()); conf = len(db.conf_abiertos())
        return f"📊 Docs: {docs} | Conflictos abiertos: {conf}"
    if cmd == "/conflictos":
        cs = db.conf_abiertos()
        if not cs: return "✅ Sin conflictos abiertos."
        return "\n".join(f"{c['id']}: [{c['proyecto']}] "
                         f"{c['doc_a'][:8]} vs {c['doc_b'][:8]} "
                         f"(sim {c['similitud']})" for c in cs[:20])
    if cmd == "/resolver" and len(p) >= 3:
        cid, dec = p[1], p[2].upper()
        c = db.conf_resolver(cid, f"resuelto_{dec}")
        if not c: return "❌ Conflicto no encontrado."
        gana = c["doc_a"] if dec == "A" else c["doc_b"]
        pierde = c["doc_b"] if dec == "A" else c["doc_a"]
        if dec in ("A", "B"):
            db.inv_estado(gana, "auditado")
            db.inv_estado(pierde, "archivado", parents=gana)
            return f"✅ {cid}: gana {gana[:8]}, {pierde[:8]} archivado."
        if dec == "FUSION":
            db.tarea_add(c["proyecto"], f"FUSIONAR {c['doc_a'][:8]}+{c['doc_b'][:8]}", "FUSION")
            return f"🔀 {cid}: fusión solicitada. Sube el doc fusionado."
        return "Uso: /resolver <id> A|B|FUSION"
    if cmd == "/frontera" and len(p) >= 2:
        pr = p[1]
        conf = len(db.conf_abiertos(pr))
        pend = len(db.inv_por(pr, "ingresado"))
        ok = conf == 0 and pend == 0 and len(db.inv_por(pr)) > 0
        return (f"{'✅ FRONTERA OK' if ok else '⏳ Pendiente'} — "
                f"{pr}: {conf} conflictos, {pend} sin auditar")
    if cmd == "/handoff" and len(p) >= 2:
        r = outputs.call("handoff", "export", {"proyecto": p[1]})
        return f"📦 Handoff: {r.get('path', r.get('error'))}"
    return ("Comandos: /estado /conflictos /resolver <id> A|B|FUSION "
            "/frontera <proyecto> /handoff <proyecto>")
