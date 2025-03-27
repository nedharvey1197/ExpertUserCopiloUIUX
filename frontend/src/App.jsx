// New Copilot Intake Flow with Step-by-Step Wizard + Reactive Tabs

import React, { useState, useEffect } from "react";
import { Card, CardContent } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Textarea } from "./components/ui/textarea";
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "./components/ui/tabs";
import { MessageCircle, ClipboardList } from "lucide-react";

export default function App() {
  const [tab, setTab] = useState("chat");
  const [step, setStep] = useState(1);

  const [companyName, setCompanyName] = useState("");
  const [website, setWebsite] = useState("");
  const [therapeuticArea, setTherapeuticArea] = useState("");
  const [phase, setPhase] = useState("");

  const [who, setWho] = useState("");
  const [what, setWhat] = useState("");
  const [where, setWhere] = useState("");
  const [when, setWhen] = useState("");
  const [why, setWhy] = useState("");
  const [copilotSummary, setCopilotSummary] = useState("");

  useEffect(() => {
    const lines = [];

    if (who) lines.push(`👥 WHO: ${who}`);
    if (what) lines.push(`💊 WHAT: ${what}`);
    if (why) lines.push(`🧠 WHY: ${why}`);
    if (!who || !what || !why) {
      lines.push("🔍 Copilot is still waiting for more info to understand the full trial picture.");
    } else {
      lines.push("✅ You're building a strong foundation. Let me know when you're ready to explore endpoints or comparators.");
    }

    setCopilotSummary(lines.join("\n"));
  }, [who, what, why, where, when]);

  const allBasicsFilled = companyName && website && therapeuticArea && phase;

  const renderStep1 = () => (
    <Card>
      <CardContent className="space-y-4">
        <h2 className="text-lg font-semibold">🔰 Step 1: Company & Trial Basics</h2>
        <Input
          placeholder="Company Name"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
        />
        <Input
          placeholder="Company Website"
          value={website}
          onChange={(e) => setWebsite(e.target.value)}
        />
        <Input
          placeholder="Therapeutic Area (e.g. Oncology)"
          value={therapeuticArea}
          onChange={(e) => setTherapeuticArea(e.target.value)}
        />
        <Input
          placeholder="Trial Phase (e.g. Phase 1, 2b...)"
          value={phase}
          onChange={(e) => setPhase(e.target.value)}
        />
        <Button
          onClick={() => setStep(2)}
          disabled={!allBasicsFilled}
        >
          Next: Define the 5Ws
        </Button>
      </CardContent>
    </Card>
  );

  const renderStep2 = () => (
    <Card>
      <CardContent className="space-y-4">
        <h2 className="text-lg font-semibold">📋 Step 2: The 5Ws of Your Trial</h2>
        <Card className="bg-blue-50 border border-blue-200">
          <CardContent>
            <h3 className="text-sm font-semibold">🤖 Copilot Summary (So Far)</h3>
            <p className="text-sm whitespace-pre-wrap">{copilotSummary}</p>
          </CardContent>
        </Card>
        <Textarea
          placeholder="👥 WHO: Describe the patient population, key demographics, condition stage, and defining traits."
          value={who}
          onChange={(e) => setWho(e.target.value)}
        />
        <Textarea
          placeholder="💊 WHAT: What intervention or therapy is being tested? Known details on dosage or delivery?"
          value={what}
          onChange={(e) => setWhat(e.target.value)}
        />
        <Textarea
          placeholder="🌍 WHERE: Trial location, geographic focus, or site model (US only, global, etc.)"
          value={where}
          onChange={(e) => setWhere(e.target.value)}
        />
        <Textarea
          placeholder="⏱️ WHEN: Timeline assumptions or known milestones?"
          value={when}
          onChange={(e) => setWhen(e.target.value)}
        />
        <Textarea
          placeholder="🧠 WHY: What's the clinical/scientific rationale behind this trial?"
          value={why}
          onChange={(e) => setWhy(e.target.value)}
        />
        <Button onClick={() => setStep(3)}>Finish Intake</Button>
      </CardContent>
    </Card>
  );

  const renderStep3 = () => (
    <Card>
      <CardContent className="space-y-2">
        <h2 className="text-lg font-semibold">✅ Copilot Summary</h2>
        <p className="text-sm whitespace-pre-wrap">
          📌 <strong>Company:</strong> {companyName}\n
          🌐 <strong>Website:</strong> {website}\n
          🧪 <strong>Therapeutic Area:</strong> {therapeuticArea}\n
          🧬 <strong>Phase:</strong> {phase}\n
          \n👥 <strong>WHO:</strong> {who}\n
          💊 <strong>WHAT:</strong> {what}\n
          🌍 <strong>WHERE:</strong> {where}\n
          ⏱️ <strong>WHEN:</strong> {when}\n
          🧠 <strong>WHY:</strong> {why}
        </p>
      </CardContent>
    </Card>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-6 space-y-6">
      <h1 className="text-2xl font-bold">🧪 Clinical Development Copilot</h1>

      <Tabs value={tab} onValueChange={(v) => {
        setTab(v);
        if (v === "dashboard") alert("🚧 Dashboard coming soon");
      }}>
        <TabsList>
          <TabsTrigger value="chat">
            <MessageCircle className="w-4 h-4 mr-2" /> Intake Flow
          </TabsTrigger>
          <TabsTrigger value="dashboard">
            <ClipboardList className="w-4 h-4 mr-2" /> Dashboard (Soon)
          </TabsTrigger>
        </TabsList>

        <TabsContent value="chat">
          {step === 1 && renderStep1()}
          {step === 2 && renderStep2()}
          {step === 3 && renderStep3()}
        </TabsContent>

        <TabsContent value="dashboard">
          <Card>
            <CardContent className="text-center text-gray-500">
              🚧 Dashboard features are coming soon. Stay tuned.
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}