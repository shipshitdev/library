# Vercel AI SDK — Complete Reference

## Installation & Setup

### Core Package
```bash
npm install ai
```

### Provider Packages
```bash
# Pick your provider(s)
npm install @ai-sdk/openai      # OpenAI / Azure OpenAI
npm install @ai-sdk/anthropic   # Anthropic Claude
npm install @ai-sdk/google      # Google Gemini
npm install @ai-sdk/mistral     # Mistral AI
npm install @ai-sdk/cohere      # Cohere
npm install @ai-sdk/amazon-bedrock  # AWS Bedrock
```

### Environment Variables
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_GENERATIVE_AI_API_KEY=...
MISTRAL_API_KEY=...
```

---

## Core Functions

### `generateText`
Non-streaming text generation. Best for server-side processing, background jobs, or when you need the full result at once.

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const { text, usage, finishReason, toolCalls, toolResults } = await generateText({
  model: openai('gpt-4o'),
  system: 'You are a helpful assistant.',
  prompt: 'Explain quantum computing in 3 sentences.',
  maxTokens: 500,
  temperature: 0.7,
  topP: 0.9,
  frequencyPenalty: 0.5,
  presencePenalty: 0.5,
  abortSignal: AbortSignal.timeout(30000),
});

console.log(text);
console.log(`Tokens: ${usage.promptTokens} in / ${usage.completionTokens} out`);
```

### `streamText`
Streaming text generation. Best for chat UIs and real-time responses.

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = streamText({
  model: openai('gpt-4o'),
  messages: [
    { role: 'user', content: 'Write a poem about coding.' },
  ],
  onChunk: ({ chunk }) => {
    // Process each chunk as it arrives
    if (chunk.type === 'text-delta') {
      process.stdout.write(chunk.textDelta);
    }
  },
  onFinish: ({ text, usage, finishReason }) => {
    // Save to DB, log analytics, etc.
    console.log(`\nDone. Tokens: ${usage.totalTokens}`);
  },
});

// For Next.js route handlers:
return result.toDataStreamResponse();

// For plain text streaming:
return result.toTextStreamResponse();

// For consuming in Node.js:
for await (const textPart of result.textStream) {
  process.stdout.write(textPart);
}
```

### `generateObject`
Generate typed, validated objects. The model output is guaranteed to match your Zod schema.

```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { object, usage } = await generateObject({
  model: openai('gpt-4o'),
  schema: z.object({
    events: z.array(z.object({
      title: z.string(),
      date: z.string().describe('ISO 8601 date'),
      importance: z.number().min(1).max(10),
      summary: z.string().max(200),
    })),
  }),
  prompt: 'List 5 key events in the history of computing.',
});

// object.events is fully typed
object.events.forEach(e => console.log(`${e.date}: ${e.title} (${e.importance}/10)`));
```

### `streamObject`
Stream structured objects progressively. UI updates as fields arrive.

```typescript
import { streamObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const result = streamObject({
  model: openai('gpt-4o'),
  schema: z.object({
    analysis: z.object({
      sentiment: z.enum(['positive', 'negative', 'neutral']),
      confidence: z.number(),
      topics: z.array(z.string()),
      summary: z.string(),
    }),
  }),
  prompt: 'Analyze the sentiment of this review: "Amazing product, changed my life!"',
});

// Partial results stream in
for await (const partial of result.partialObjectStream) {
  console.clear();
  console.log(JSON.stringify(partial, null, 2));
}

// Final validated object
const { object } = await result;
```

---

## React Hooks

### `useChat`
Full-featured chat hook with streaming, tool handling, and state management.

```tsx
'use client';
import { useChat } from '@ai-sdk/react';

export function ChatComponent() {
  const {
    messages,        // Message[]
    input,           // string - controlled input value
    handleInputChange, // onChange handler
    handleSubmit,    // onSubmit handler
    isLoading,       // boolean
    stop,            // () => void - stop streaming
    reload,          // () => void - regenerate last response
    error,           // Error | undefined
    setMessages,     // (messages: Message[]) => void
    append,          // (message: Message) => void
  } = useChat({
    api: '/api/chat',                    // endpoint (default: /api/chat)
    initialMessages: [],                 // pre-populate conversation
    body: { userId: 'abc' },             // extra body params sent with each request
    headers: { 'X-Custom': 'value' },    // custom headers
    onResponse: (response) => {},        // when response starts
    onFinish: (message) => {},           // when response completes
    onError: (error) => {},              // on error
    maxSteps: 5,                         // allow multi-step tool use
  });

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`rounded-lg px-4 py-2 max-w-[80%] ${
              m.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100'
            }`}>
              {m.content}
              {m.toolInvocations?.map((tool, i) => (
                <pre key={i} className="text-xs mt-2 bg-gray-200 p-2 rounded">
                  {tool.toolName}: {JSON.stringify(tool.result, null, 2)}
                </pre>
              ))}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          className="flex-1 border rounded px-3 py-2"
          placeholder="Type a message..."
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Thinking...' : 'Send'}
        </button>
        {isLoading && <button type="button" onClick={stop}>Stop</button>}
      </form>
      {error && <div className="p-2 text-red-500">{error.message}</div>}
    </div>
  );
}
```

### `useCompletion`
For single-turn completions (not multi-message chat).

```tsx
'use client';
import { useCompletion } from '@ai-sdk/react';

export function CompletionComponent() {
  const { completion, input, handleInputChange, handleSubmit, isLoading } = useCompletion({
    api: '/api/completion',
  });

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} placeholder="Enter prompt..." />
        <button type="submit" disabled={isLoading}>Generate</button>
      </form>
      <div>{completion}</div>
    </div>
  );
}
```

### `useObject`
Stream structured objects into React state.

```tsx
'use client';
import { useObject } from '@ai-sdk/react';
import { z } from 'zod';

const notificationSchema = z.object({
  notifications: z.array(z.object({
    name: z.string(),
    message: z.string(),
    priority: z.enum(['low', 'medium', 'high']),
  })),
});

export function NotificationGenerator() {
  const { object, submit, isLoading } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <div>
      <button onClick={() => submit('Generate 5 notifications')} disabled={isLoading}>
        Generate
      </button>
      {object?.notifications?.map((n, i) => (
        <div key={i} className={`p-2 border-l-4 ${
          n?.priority === 'high' ? 'border-red-500' : 
          n?.priority === 'medium' ? 'border-yellow-500' : 'border-green-500'
        }`}>
          <strong>{n?.name}</strong>: {n?.message}
        </div>
      ))}
    </div>
  );
}
```

---

## Tool Calling (Advanced)

### Defining Tools

```typescript
import { tool } from 'ai';
import { z } from 'zod';

const tools = {
  searchDocuments: tool({
    description: 'Search the knowledge base for relevant documents',
    parameters: z.object({
      query: z.string().describe('Search query'),
      limit: z.number().optional().default(5).describe('Max results'),
    }),
    execute: async ({ query, limit }) => {
      const results = await db.search(query, limit);
      return results;
    },
  }),

  createTask: tool({
    description: 'Create a new task in the project management system',
    parameters: z.object({
      title: z.string(),
      priority: z.enum(['low', 'medium', 'high']),
      assignee: z.string().optional(),
    }),
    execute: async ({ title, priority, assignee }) => {
      const task = await projectManager.createTask({ title, priority, assignee });
      return { id: task.id, url: task.url };
    },
  }),

  // Tool with no execute — requires human confirmation
  deleteAccount: tool({
    description: 'Delete a user account (requires confirmation)',
    parameters: z.object({
      userId: z.string(),
      reason: z.string(),
    }),
    // No execute — will pause for human-in-the-loop
  }),
};
```

### Multi-Step Tool Use

```typescript
const result = await generateText({
  model: openai('gpt-4o'),
  tools,
  maxSteps: 10, // Allow up to 10 tool call rounds
  onStepFinish: ({ text, toolCalls, toolResults, finishReason, usage }) => {
    console.log('Step finished:', { toolCalls: toolCalls?.length, finishReason });
  },
  prompt: 'Search for documents about deployment, then create a task to update the docs.',
});

// result.steps contains all intermediate steps
result.steps.forEach((step, i) => {
  console.log(`Step ${i}: ${step.toolCalls?.length ?? 0} tool calls`);
});
```

---

## Embeddings

```typescript
import { embed, embedMany, cosineSimilarity } from 'ai';
import { openai } from '@ai-sdk/openai';

const embeddingModel = openai.embedding('text-embedding-3-small');

// Single embedding
const { embedding } = await embed({
  model: embeddingModel,
  value: 'Hello world',
});

// Batch embeddings (more efficient)
const { embeddings } = await embedMany({
  model: embeddingModel,
  values: ['Hello', 'World', 'Foo', 'Bar'],
});

// Similarity search
const similarity = cosineSimilarity(embedding1, embedding2);
```

---

## Production Patterns

### Error Handling & Retries

```typescript
import { generateText, APICallError } from 'ai';

async function generateWithRetry(prompt: string, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await generateText({
        model: openai('gpt-4o'),
        prompt,
        abortSignal: AbortSignal.timeout(30000),
      });
    } catch (error) {
      if (error instanceof APICallError && error.statusCode === 429) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Rate Limiting API Routes

```typescript
// app/api/chat/route.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'), // 10 requests per minute
});

export async function POST(req: Request) {
  const ip = req.headers.get('x-forwarded-for') ?? '127.0.0.1';
  const { success } = await ratelimit.limit(ip);
  if (!success) return new Response('Too many requests', { status: 429 });

  // ... handle AI request
}
```

### Token Usage Tracking

```typescript
const result = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Hello',
  onFinish: async ({ usage }) => {
    await db.usageLogs.create({
      data: {
        userId,
        promptTokens: usage.promptTokens,
        completionTokens: usage.completionTokens,
        model: 'gpt-4o',
        cost: calculateCost('gpt-4o', usage),
        timestamp: new Date(),
      },
    });
  },
});
```

### Caching Responses

```typescript
import { generateText } from 'ai';
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

async function cachedGenerate(prompt: string) {
  const cacheKey = `ai:${hashPrompt(prompt)}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const result = await generateText({
    model: openai('gpt-4o'),
    prompt,
  });

  await redis.setex(cacheKey, 3600, JSON.stringify({ text: result.text }));
  return { text: result.text };
}
```

---

## Next.js App Router Integration

### Route Handler Pattern

```
app/
├── api/
│   ├── chat/
│   │   └── route.ts          # POST — streaming chat
│   ├── completion/
│   │   └── route.ts          # POST — single completion
│   └── objects/
│       └── route.ts          # POST — structured output
├── chat/
│   └── page.tsx              # Chat UI with useChat
└── layout.tsx
```

### Middleware for Auth

```typescript
// middleware.ts
export function middleware(req: NextRequest) {
  if (req.nextUrl.pathname.startsWith('/api/chat')) {
    const token = req.headers.get('authorization')?.replace('Bearer ', '');
    if (!token || !verifyToken(token)) {
      return new Response('Unauthorized', { status: 401 });
    }
  }
}
```

---

## Common Gotchas

1. **Don't forget `runtime = 'edge'`** — Without it, streaming may buffer on Vercel
2. **`useChat` sends full message history** — Trim old messages to control costs
3. **Tool results must be serializable** — No functions, circular refs, or Dates
4. **`maxSteps` defaults to 1** — Set higher for multi-step tool use
5. **Provider API keys in `.env.local`** — Never commit or expose client-side
6. **Abort signals** — Always pass `req.signal` in route handlers to cancel on disconnect
