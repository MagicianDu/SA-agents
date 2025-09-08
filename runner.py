
import os, sys, yaml, json, re, pathlib, argparse
import xml.etree.ElementTree as ET

def load_openai():
    try:
        from openai import OpenAI
        return OpenAI()
    except Exception:
        return None

def run_llm(system_prompt:str, user_input:str, model:str):
    client = load_openai()
    if client is None:
        raise RuntimeError("OpenAI SDK 未安装。请先: pip install openai")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("缺少 OPENAI_API_KEY 环境变量。")

    resp = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_input}
        ]
    )
    return resp.choices[0].message.content

def substitute_vars(xml_text:str, vars:dict)->str:
    def repl(m):
        key = m.group(1)
        return str(vars.get(key, f"${{{key}}}"))
    return re.sub(r"\$\{([A-Z0-9_]+)\}", repl, xml_text)

def read_file(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def write_file(p, content:str):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def parse_bundle(xml_text:str):
    start = xml_text.find("<bundle")
    end = xml_text.find("</bundle>")
    if start == -1 or end == -1:
        raise ValueError("未找到 <bundle> 包裹。")
    xml = xml_text[start:end+9]
    root = ET.fromstring(xml)
    outs = []
    for d in root.findall(".//deliverable"):
        name = d.attrib.get("name","unnamed.txt")
        content = d.text or ""
        outs.append((name, content))
    return outs

def task_context(init_vars, inputs):
    ctx = {"INIT_VARS": init_vars, "INPUT_FILES": []}
    for p in inputs or []:
        if os.path.exists(p):
            ctx["INPUT_FILES"].append({"path": p, "content": read_file(p)})
        else:
            ctx["INPUT_FILES"].append({"path": p, "content": f"[MISSING] {p}"})
    return ctx

def build_user_prompt(ctx:dict)->str:
    parts = []
    parts.append("# 任务上下文\n")
    parts.append("## 起点变量\n")
    parts.append(json.dumps(ctx["INIT_VARS"], ensure_ascii=False, indent=2))
    parts.append("\n## 上游输入文件\n")
    for f in ctx["INPUT_FILES"]:
        parts.append(f"\n--- file: {f['path']} ---\n")
        parts.append(f"{f['content']}\n")
    parts.append("\n## 请严格按系统提示产出 <bundle>。\n")
    return "\n".join(parts)

def topo_order(tasks):
    by_id = {t["id"]: t for t in tasks}
    indeg = {t["id"]:0 for t in tasks}
    for t in tasks:
        for d in t.get("depends_on",[]) or []:
            indeg[t["id"]] += 1
    q = [tid for tid,deg in indeg.items() if deg==0]
    res = []
    while q:
        tid = q.pop(0)
        res.append(by_id[tid])
        for t in tasks:
            if tid in (t.get("depends_on") or []):
                indeg[t["id"]] -= 1
                if indeg[t["id"]]==0:
                    q.append(t["id"])
    return res

def load_init_vars(p):
    with open(p,"r",encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", default="project_init.yaml")
    ap.add_argument("--workflow", default="workflow.yaml")
    ap.add_argument("--model", default=os.environ.get("OPENAI_MODEL","gpt-4o-mini"))
    args = ap.parse_args()

    with open(args.workflow,"r",encoding="utf-8") as f:
        wf = yaml.safe_load(f)

    out_dir = wf.get("out_dir","out")
    os.makedirs(out_dir, exist_ok=True)

    init_vars = load_init_vars(args.init)
    tasks = wf["tasks"]
    order = topo_order(tasks)

    for t in order:
        tid = t["id"]
        sys_prompt = read_file(t["prompt"])
        sys_prompt = substitute_vars(sys_prompt, init_vars)

        ins = []
        for inp in t.get("inputs") or []:
            if isinstance(inp, dict) and "init" in inp:
                pass
            else:
                ins.append(inp)

        ctx = task_context(init_vars, ins)
        user_prompt = build_user_prompt(ctx)

        print(f"[RUN] {tid} using {t['agent']} ...")
        content = run_llm(sys_prompt, user_prompt, args.model)

        bundle = parse_bundle(content)
        task_dir = os.path.join(out_dir, tid)
        for name, cnt in bundle:
            out_path = os.path.join(task_dir, name)
            write_file(out_path, cnt)
            print("  ->", out_path)

        if t.get("gate"):
            status = None
            for name, cnt in bundle:
                if name.endswith(".xml"):
                    try:
                        g = ET.fromstring(cnt)
                        status = g.attrib.get("status","yellow")
                        break
                    except:
                        pass
            if status is None:
                raise RuntimeError(f"{tid} 未返回 gate XML 或无法解析。")
            print(f"  [GATE] {tid} status = {status}")
            if status.lower() == "red":
                print("  [STOP] Gate 红灯，终止执行。")
                sys.exit(2)

    print("\n[OK] 工作流完成。输出目录：", out_dir)

if __name__ == "__main__":
    main()
