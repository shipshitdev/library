import { vi } from "vitest";
import "@testing-library/jest-dom/vitest";

// Mock environment variables for tests
process.env.NODE_ENV = "test";

// Mock Next.js router
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
  }),
  usePathname: () => "/",
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({}),
}));

// Mock Next.js Image component
vi.mock("next/image", () => ({
  default: ({ src, alt, ...props }: { src: string; alt: string }) => {
    // eslint-disable-next-line @next/next/no-img-element
    return `<img src="${src}" alt="${alt}" />`;
  },
}));

// Reset mocks between tests
beforeEach(() => {
  vi.clearAllMocks();
});
