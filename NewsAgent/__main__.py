import argparse
from datetime import datetime
try:
    from .agent import *
except:
    from agent import *

def parse_args():
    p = argparse.ArgumentParser(prog="NewsAgent", description="News Agent")
    p.add_argument("-t", "--text-file", help="Output to Text file", action="store_true")
    p.add_argument("--html", help="Output to HTML File", action="store_true")
    p.add_argument("-p", "--plain", help="Output to Screen", action="store_true")
    p.add_argument("-x", "--xml", help="Output to XML File", action="store_true")
    args = p.parse_args()
    return args

agent = NewsAgent()
args = parse_args()

if args.text_file:
    agent.addDestination(TextFileDestination(str(datetime.now())[0:10]+"-news.txt"))

if args.html:
    agent.addDestination(HTMLDestination(str(datetime.now())[0:10]+"-news.htm"))
    
if args.plain:
    agent.addDestination(PlainDestination())

if args.xml:
    agent.addDestination(XMLDestination(str(datetime.now())[0:10]+"-news.xml"))

agent.add_source(NNTPSource("comp.lang.python.announce", 5))
agent.add_source(NNTPSource("aus.politics", 5))
agent.add_source(NNTPSource("comp.lang.python", 5))
agent.add_source(NNTPSource("alt.math", 5))
agent.add_source(NNTPSource("alt.physics", 5))
agent.add_source(FoxNewsSource())

print("Distributing...")

agent.distribute()

print("Done.")