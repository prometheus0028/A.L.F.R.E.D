/**
 * Mock API for ALFRED Frontend
 * Simulates backend responses and SSE events.
 */

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

let activeTask = null;
let eventSubscribers = [];

const dispatchEvent = (event) => {
  eventSubscribers.forEach(sub => sub(event));
};

export const createTask = async (goal) => {
  await delay(500);
  activeTask = {
    task_id: "task_demo_001",
    status: "created",
    goal: goal,
    current_step: 0,
    total_steps: 0,
    plan: [],
    actions: [],
    approval: null,
    result: null,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  
  // Start mock sequence
  setTimeout(() => runMockSequence(goal), 100);

  return {
    task_id: activeTask.task_id,
    status: activeTask.status,
    goal: activeTask.goal
  };
};

export const getTask = async (taskId) => {
  await delay(200);
  if (!activeTask || activeTask.task_id !== taskId) {
    throw new Error("TASK_NOT_FOUND");
  }
  return { ...activeTask };
};

export const approveAction = async (taskId, approvalId) => {
  await delay(300);
  if (!activeTask || activeTask.task_id !== taskId) throw new Error("TASK_NOT_FOUND");
  
  activeTask.status = "executing";
  activeTask.approval = null;
  
  // Resume sequence for finance
  setTimeout(runFinanceCompletion, 500);

  return { task_id: taskId, status: "executing", message: "Approval accepted." };
};

export const rejectAction = async (taskId, approvalId, reason) => {
  await delay(300);
  if (!activeTask || activeTask.task_id !== taskId) throw new Error("TASK_NOT_FOUND");
  
  activeTask.status = "failed";
  activeTask.approval = null;
  
  dispatchEvent({
    type: "task_failed",
    task_id: taskId,
    timestamp: new Date().toISOString(),
    data: { message: "Payment was rejected by the user." }
  });

  return { task_id: taskId, status: "failed", message: "Payment was rejected by the user." };
};

export const subscribeToTaskEvents = (taskId, callback) => {
  eventSubscribers.push(callback);
  return () => {
    eventSubscribers = eventSubscribers.filter(sub => sub !== callback);
  };
};

// --- Mock Sequences ---

const runMockSequence = async (goal) => {
  const isFinance = goal.toLowerCase().includes("invoice") || goal.toLowerCase().includes("policy");
  
  activeTask.status = "executing";
  dispatchEvent({
    type: "goal_received",
    task_id: activeTask.task_id,
    timestamp: new Date().toISOString(),
    data: { goal: activeTask.goal }
  });

  await delay(1000);
  
  if (isFinance) {
    await runFinanceSequence();
  } else {
    await runMeetingSequence();
  }
};

const runMeetingSequence = async () => {
  activeTask.total_steps = 5;
  activeTask.plan = [
    { id: "step_1", description: "Find the meeting with Rahul", tool: "calendar.search", status: "pending" },
    { id: "step_2", description: "Search relevant emails", tool: "email.search", status: "pending" },
    { id: "step_3", description: "Find latest project document", tool: "files.search", status: "pending" },
    { id: "step_4", description: "Create briefing", tool: "documents.create", status: "pending" },
    { id: "step_5", description: "Verify briefing exists", tool: "files.search", status: "pending" }
  ];
  
  dispatchEvent({
    type: "plan_created",
    task_id: activeTask.task_id,
    timestamp: new Date().toISOString(),
    data: { step_count: 5 }
  });

  await delay(800);

  // Step 1: Calendar
  updateStep("step_1", "running");
  dispatchEvent({ type: "tool_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "calendar", operation: "search" } });
  await delay(800);
  addAction("action_001", "calendar", "search", "completed", "Found Rahul project review");
  updateStep("step_1", "completed");
  dispatchEvent({ type: "tool_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "calendar", operation: "search", summary: "Found Rahul project review", success: true } });

  await delay(600);

  // Step 2: Email
  updateStep("step_2", "running");
  dispatchEvent({ type: "tool_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "email", operation: "search" } });
  await delay(1200);
  addAction("action_002", "email", "search", "completed", "Found 4 relevant messages");
  updateStep("step_2", "completed");
  dispatchEvent({ type: "tool_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "email", operation: "search", summary: "Found 4 relevant messages", success: true } });

  await delay(800);

  // Step 3: Files (Intentional Failure & Recovery)
  updateStep("step_3", "running");
  dispatchEvent({ type: "tool_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "files", operation: "search" } });
  await delay(1000);
  activeTask.status = "replanning";
  dispatchEvent({ type: "replanning", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { reason: "No exact document found", attempt: 1, message: "Searching project status documents instead." } });
  await delay(1500);
  activeTask.status = "executing";
  addAction("action_003", "files", "search", "completed", "Found project status document");
  updateStep("step_3", "completed");
  dispatchEvent({ type: "tool_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "files", operation: "search", summary: "Found project status document", success: true } });

  await delay(600);

  // Step 4: Document
  updateStep("step_4", "running");
  dispatchEvent({ type: "tool_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "documents", operation: "create" } });
  await delay(1500);
  addAction("action_004", "documents", "create", "completed", "Created meeting_brief.md");
  updateStep("step_4", "completed");
  dispatchEvent({ type: "tool_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "documents", operation: "create", summary: "Created meeting_brief.md", success: true } });

  await delay(600);
  
  // Step 5: Verification
  updateStep("step_5", "running");
  dispatchEvent({ type: "verification_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: {} });
  await delay(1000);
  updateStep("step_5", "completed");
  dispatchEvent({ type: "verification_passed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: {} });

  activeTask.status = "completed";
  activeTask.result = {
    type: "meeting_brief",
    status: "verified",
    title: "Meeting briefing created",
    file_name: "meeting_brief.md",
    summary: "Briefing created and verified.",
    evidence: ["1 calendar event", "4 emails", "2 documents"]
  };
  dispatchEvent({ type: "task_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { summary: "Meeting briefing created and verified." } });
};

const runFinanceSequence = async () => {
  activeTask.total_steps = 3;
  activeTask.plan = [
    { id: "step_1", description: "Find pending invoice", tool: "finance.list_pending_invoices", status: "pending" },
    { id: "step_2", description: "Check policy and propose payment", tool: "finance.propose_payment", status: "pending" },
    { id: "step_3", description: "Execute transaction", tool: "blockchain.adapter", status: "pending" }
  ];
  
  dispatchEvent({ type: "plan_created", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { step_count: 3 } });
  await delay(1000);

  // Step 1
  updateStep("step_1", "running");
  dispatchEvent({ type: "tool_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "finance", operation: "list_pending_invoices" } });
  await delay(800);
  addAction("action_001", "finance", "list_pending_invoices", "completed", "Found invoice INV-1042");
  updateStep("step_1", "completed");
  dispatchEvent({ type: "tool_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "finance", operation: "list_pending_invoices", summary: "Found invoice INV-1042", success: true } });

  await delay(800);

  // Step 2 & Approval Required
  updateStep("step_2", "running");
  dispatchEvent({ type: "tool_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "finance", operation: "check_policy" } });
  await delay(1200);
  activeTask.status = "waiting_approval";
  activeTask.approval = {
    approval_id: "approval_001",
    type: "payment",
    status: "pending",
    title: "Payment requires approval",
    vendor: "Acme Supplies",
    amount: 3800,
    currency: "INR",
    invoice_id: "INV-1042",
    policy: {
      result: "APPROVAL_REQUIRED",
      vendor_approved: true,
      within_limit: true,
      limit: 5000
    }
  };
  dispatchEvent({ type: "approval_required", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { approval: activeTask.approval } });
};

const runFinanceCompletion = async () => {
  addAction("action_002", "finance", "propose_payment", "completed", "Payment proposed and approved");
  updateStep("step_2", "completed");
  dispatchEvent({ type: "tool_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "finance", operation: "propose_payment", summary: "Payment proposed and approved", success: true } });

  await delay(1000);

  updateStep("step_3", "running");
  dispatchEvent({ type: "tool_started", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { tool: "blockchain", operation: "execute" } });
  await delay(2000);
  
  activeTask.status = "completed";
  updateStep("step_3", "completed");
  activeTask.result = {
    type: "payment",
    status: "verified",
    vendor: "Acme Supplies",
    amount: 3800,
    currency: "INR",
    transaction_hash: "0xDEMO827361ABCD...",
    evidence: ["Policy passed", "User approved", "Transaction confirmed"]
  };
  addAction("action_003", "blockchain", "execute", "completed", "Transaction confirmed: 0xDEMO...");
  dispatchEvent({ type: "task_completed", task_id: activeTask.task_id, timestamp: new Date().toISOString(), data: { summary: "Payment verified and executed." } });
};

const updateStep = (stepId, status) => {
  const step = activeTask.plan.find(s => s.id === stepId);
  if (step) step.status = status;
};

const addAction = (id, tool, operation, status, summary) => {
  activeTask.actions.push({ id, tool, operation, status, summary });
};
