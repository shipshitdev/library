---
name: stripe-implementer
description: Guide for implementing Stripe payment processing, subscription management, webhook handling, and customer management in Next.js or NestJS applications. Use when users need Stripe integration, payment processing, subscriptions, webhooks, or Stripe API implementation.
---
# Stripe Implementer

## Overview

To implement comprehensive Stripe integrations including payment processing, subscription management, webhook handling, and customer management for Next.js and NestJS applications. Codex determines when this skill is needed based on Stripe-related implementation tasks.

## When to Use This Skill

Use when users need:

- Need to integrate Stripe payments into their application
- Want to implement subscription billing
- Need to set up Stripe webhooks
- Want to manage Stripe customers
- Need to handle payment intents or checkout sessions
- Want to implement Stripe Connect or marketplace features
- Need to handle refunds or disputes

## Project Context Discovery

Before implementing Stripe integration:

1. **Scan Project Documentation:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for payment architecture
   - Review existing API patterns
   - Look for environment variable usage
   - Check for existing Stripe integration

2. **Identify Framework:**
   - Determine if using Next.js (App Router or Pages Router)
   - Check if using NestJS backend
   - Review existing API route patterns
   - Check authentication/authorization setup

3. **Use Project-Specific Skills:**
   - Check for `[project]-stripe-implementer` skill
   - Review project-specific payment patterns
   - Follow project's API standards

## Setup and Configuration

### 1. Install Stripe SDK

**Next.js:**
```bash
npm install stripe @stripe/stripe-js
# or
yarn add stripe @stripe/stripe-js
```

**NestJS:**
```bash
npm install stripe
# or
yarn add stripe
```

### 2. Environment Variables

Create `.env.local` (Next.js) or `.env` (NestJS):

```env
# Stripe API Keys
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Use test keys for development, live keys for production
```

### 3. Initialize Stripe Client

**Next.js API Route (Server-side):**

```typescript
// app/api/stripe/route.ts or pages/api/stripe/index.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});
```

**Next.js Client-side:**

```typescript
// components/stripe-provider.tsx
'use client';

import { loadStripe } from '@stripe/stripe-js';

export const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);
```

**NestJS Service:**

```typescript
// src/stripe/stripe.service.ts
import { Injectable } from '@nestjs/common';
import Stripe from 'stripe';

@Injectable()
export class StripeService {
  private stripe: Stripe;

  constructor() {
    this.stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: '2024-12-18.acacia',
    });
  }

  getStripe(): Stripe {
    return this.stripe;
  }
}
```

## Payment Processing

### 1. Checkout Sessions (Recommended for One-time Payments)

**Next.js App Router:**

```typescript
// app/api/checkout/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

export async function POST(request: NextRequest) {
  try {
    const { amount, currency = 'usd', successUrl, cancelUrl } = await request.json();

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency,
            product_data: {
              name: 'Product Name',
            },
            unit_amount: amount, // Amount in cents
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: successUrl || `${request.headers.get('origin')}/success`,
      cancel_url: cancelUrl || `${request.headers.get('origin')}/cancel`,
    });

    return NextResponse.json({ sessionId: session.id });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create checkout session' },
      { status: 500 }
    );
  }
}
```

**Next.js Client Component:**

```typescript
// components/checkout-button.tsx
'use client';

import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export function CheckoutButton({ amount }: { amount: number }) {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount }),
      });

      const { sessionId } = await response.json();
      const stripe = await stripePromise;
      
      await stripe?.redirectToCheckout({ sessionId });
    } catch (error) {
      console.error('Checkout error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleCheckout} disabled={loading}>
      {loading ? 'Processing...' : 'Checkout'}
    </button>
  );
}
```

**NestJS Controller:**

```typescript
// src/stripe/stripe.controller.ts
import { Controller, Post, Body } from '@nestjs/common';
import { StripeService } from './stripe.service';

@Controller('stripe')
export class StripeController {
  constructor(private stripeService: StripeService) {}

  @Post('checkout')
  async createCheckoutSession(@Body() body: { amount: number; currency?: string }) {
    const stripe = this.stripeService.getStripe();

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: body.currency || 'usd',
            product_data: {
              name: 'Product Name',
            },
            unit_amount: body.amount,
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${process.env.FRONTEND_URL}/success`,
      cancel_url: `${process.env.FRONTEND_URL}/cancel`,
    });

    return { sessionId: session.id };
  }
}
```

### 2. Payment Intents (For Custom Payment Flows)

**Next.js API Route:**

```typescript
// app/api/payment-intent/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

export async function POST(request: NextRequest) {
  try {
    const { amount, currency = 'usd' } = await request.json();

    const paymentIntent = await stripe.paymentIntents.create({
      amount,
      currency,
      automatic_payment_methods: {
        enabled: true,
      },
    });

    return NextResponse.json({
      clientSecret: paymentIntent.client_secret,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create payment intent' },
      { status: 500 }
    );
  }
}
```

**NestJS Service:**

```typescript
// src/stripe/stripe.service.ts
async createPaymentIntent(amount: number, currency: string = 'usd') {
  const paymentIntent = await this.stripe.paymentIntents.create({
    amount,
    currency,
    automatic_payment_methods: {
      enabled: true,
    },
  });

  return {
    clientSecret: paymentIntent.client_secret,
    id: paymentIntent.id,
  };
}
```

## Subscription Management

### 1. Create Subscription

**Next.js API Route:**

```typescript
// app/api/subscriptions/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

export async function POST(request: NextRequest) {
  try {
    const { customerId, priceId } = await request.json();

    const subscription = await stripe.subscriptions.create({
      customer: customerId,
      items: [{ price: priceId }],
      payment_behavior: 'default_incomplete',
      payment_settings: { save_default_payment_method: 'on_subscription' },
      expand: ['latest_invoice.payment_intent'],
    });

    return NextResponse.json({
      subscriptionId: subscription.id,
      clientSecret: (subscription.latest_invoice as any).payment_intent.client_secret,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create subscription' },
      { status: 500 }
    );
  }
}
```

**NestJS Service:**

```typescript
// src/stripe/stripe.service.ts
async createSubscription(customerId: string, priceId: string) {
  const subscription = await this.stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: 'default_incomplete',
    payment_settings: { save_default_payment_method: 'on_subscription' },
    expand: ['latest_invoice.payment_intent'],
  });

  return {
    subscriptionId: subscription.id,
    clientSecret: (subscription.latest_invoice as Stripe.Invoice).payment_intent?.client_secret,
  };
}
```

### 2. Create Products and Prices

**Next.js API Route:**

```typescript
// app/api/products/route.ts
export async function POST(request: NextRequest) {
  try {
    const { name, amount, currency = 'usd', interval } = await request.json();

    // Create product
    const product = await stripe.products.create({
      name,
    });

    // Create price
    const price = await stripe.prices.create({
      product: product.id,
      unit_amount: amount,
      currency,
      recurring: interval ? { interval } : undefined,
    });

    return NextResponse.json({ productId: product.id, priceId: price.id });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create product' },
      { status: 500 }
    );
  }
}
```

### 3. Manage Subscriptions

**Cancel Subscription:**

```typescript
// Cancel immediately
await stripe.subscriptions.cancel(subscriptionId);

// Cancel at period end
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: true,
});
```

**Update Subscription:**

```typescript
await stripe.subscriptions.update(subscriptionId, {
  items: [{
    id: subscriptionItemId,
    price: newPriceId,
  }],
  proration_behavior: 'create_prorations',
});
```

## Customer Management

### 1. Create Customer

**Next.js API Route:**

```typescript
// app/api/customers/route.ts
export async function POST(request: NextRequest) {
  try {
    const { email, name, metadata } = await request.json();

    const customer = await stripe.customers.create({
      email,
      name,
      metadata,
    });

    return NextResponse.json({ customerId: customer.id });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create customer' },
      { status: 500 }
    );
  }
}
```

**NestJS Service:**

```typescript
async createCustomer(email: string, name?: string, metadata?: Record<string, string>) {
  return await this.stripe.customers.create({
    email,
    name,
    metadata,
  });
}
```

### 2. Retrieve Customer

```typescript
const customer = await stripe.customers.retrieve(customerId);
```

### 3. Update Customer

```typescript
await stripe.customers.update(customerId, {
  email: newEmail,
  name: newName,
  metadata: { key: 'value' },
});
```

## Webhook Handling

### 1. Stripe CLI Setup (Development)

```bash
# Install Stripe CLI
# macOS
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```

### 2. Webhook Endpoint (Next.js)

```typescript
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { headers } from 'next/headers';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(request: NextRequest) {
  const body = await request.text();
  const headersList = await headers();
  const signature = headersList.get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    return NextResponse.json(
      { error: 'Webhook signature verification failed' },
      { status: 400 }
    );
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      // Handle successful payment
      console.log('Payment succeeded:', paymentIntent.id);
      break;

    case 'customer.subscription.created':
      const subscription = event.data.object as Stripe.Subscription;
      // Handle subscription creation
      console.log('Subscription created:', subscription.id);
      break;

    case 'customer.subscription.updated':
      const updatedSubscription = event.data.object as Stripe.Subscription;
      // Handle subscription update
      console.log('Subscription updated:', updatedSubscription.id);
      break;

    case 'customer.subscription.deleted':
      const deletedSubscription = event.data.object as Stripe.Subscription;
      // Handle subscription cancellation
      console.log('Subscription deleted:', deletedSubscription.id);
      break;

    case 'invoice.payment_succeeded':
      const invoice = event.data.object as Stripe.Invoice;
      // Handle successful invoice payment
      console.log('Invoice paid:', invoice.id);
      break;

    case 'invoice.payment_failed':
      const failedInvoice = event.data.object as Stripe.Invoice;
      // Handle failed invoice payment
      console.log('Invoice payment failed:', failedInvoice.id);
      break;

    default:
      console.log(`Unhandled event type: ${event.type}`);
  }

  return NextResponse.json({ received: true });
}

// Disable body parsing for webhooks
export const runtime = 'nodejs';
```

### 3. Webhook Endpoint (NestJS)

```typescript
// src/stripe/stripe.controller.ts
import { Controller, Post, Body, Headers, RawBodyRequest, Req } from '@nestjs/common';
import { StripeService } from './stripe.service';
import { Request } from 'express';
import Stripe from 'stripe';

@Controller('webhooks/stripe')
export class StripeWebhookController {
  constructor(private stripeService: StripeService) {}

  @Post()
  async handleWebhook(
    @Req() request: RawBodyRequest<Request>,
    @Headers('stripe-signature') signature: string,
  ) {
    const stripe = this.stripeService.getStripe();
    const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

    let event: Stripe.Event;

    try {
      event = stripe.webhooks.constructEvent(
        request.rawBody!,
        signature,
        webhookSecret,
      );
    } catch (err) {
      throw new Error('Webhook signature verification failed');
    }

    // Handle the event
    switch (event.type) {
      case 'payment_intent.succeeded':
        await this.handlePaymentIntentSucceeded(event.data.object as Stripe.PaymentIntent);
        break;

      case 'customer.subscription.created':
        await this.handleSubscriptionCreated(event.data.object as Stripe.Subscription);
        break;

      case 'customer.subscription.updated':
        await this.handleSubscriptionUpdated(event.data.object as Stripe.Subscription);
        break;

      case 'customer.subscription.deleted':
        await this.handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return { received: true };
  }

  private async handlePaymentIntentSucceeded(paymentIntent: Stripe.PaymentIntent) {
    // Implement payment success logic
  }

  private async handleSubscriptionCreated(subscription: Stripe.Subscription) {
    // Implement subscription creation logic
  }

  private async handleSubscriptionUpdated(subscription: Stripe.Subscription) {
    // Implement subscription update logic
  }

  private async handleSubscriptionDeleted(subscription: Stripe.Subscription) {
    // Implement subscription deletion logic
  }
}
```

**NestJS Middleware for Raw Body:**

```typescript
// src/stripe/stripe.module.ts
import { Module, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { json } from 'express';

@Module({
  // ...
})
export class StripeModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(json({ verify: (req: any, res, buf) => { req.rawBody = buf; } }))
      .forRoutes('webhooks/stripe');
  }
}
```

## Best Practices

### Security
- Never expose secret keys in client-side code
- Always verify webhook signatures
- Use HTTPS for all API calls
- Store API keys in environment variables
- Implement idempotency keys for critical operations

### Error Handling
- Always handle Stripe API errors gracefully
- Use try-catch blocks for all Stripe operations
- Provide meaningful error messages to users
- Log errors for debugging
- Implement retry logic for transient failures

### Idempotency
- Use idempotency keys for payment and subscription creation
- Prevent duplicate charges or subscriptions
- Store idempotency keys with operations

```typescript
await stripe.paymentIntents.create({
  amount: 2000,
  currency: 'usd',
}, {
  idempotencyKey: uniqueIdempotencyKey,
});
```

### Testing
- Use Stripe test mode keys for development
- Test webhook handling with Stripe CLI
- Use test card numbers from Stripe documentation
- Test failure scenarios (declined cards, insufficient funds)

### Performance
- Cache product and price data when possible
- Use Stripe's expand parameter to reduce API calls
- Implement pagination for list operations
- Use webhooks instead of polling for status updates

## Common Stripe Events

- `payment_intent.succeeded` - Payment completed successfully
- `payment_intent.payment_failed` - Payment failed
- `customer.subscription.created` - New subscription created
- `customer.subscription.updated` - Subscription updated
- `customer.subscription.deleted` - Subscription canceled
- `invoice.payment_succeeded` - Invoice paid
- `invoice.payment_failed` - Invoice payment failed
- `charge.refunded` - Refund processed
- `customer.created` - New customer created
- `customer.updated` - Customer updated

## Example User Requests

**Example 1: "Add Stripe checkout to my Next.js app"**
- Set up Stripe SDK and environment variables
- Create checkout session API route
- Implement checkout button component
- Handle success/cancel pages

**Example 2: "Implement subscription billing in NestJS"**
- Set up Stripe service and module
- Create products and prices
- Implement subscription creation endpoint
- Set up webhook handling for subscription events

**Example 3: "Handle Stripe webhooks for payment status"**
- Create webhook endpoint
- Verify webhook signatures
- Handle payment success/failure events
- Update database records based on events