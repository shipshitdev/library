import { test, expect } from "@playwright/test";

test.describe("Homepage", () => {
  test("should load successfully", async ({ page }) => {
    await page.goto("/");

    // Check that the page has a title
    await expect(page).toHaveTitle(/.+/);

    // Check that the main content is visible
    await expect(page.locator("main")).toBeVisible();
  });

  test("should have working navigation", async ({ page }) => {
    await page.goto("/");

    // Find all navigation links
    const navLinks = page.locator("nav a");
    const count = await navLinks.count();

    // Verify navigation exists
    expect(count).toBeGreaterThan(0);
  });

  test("should be responsive", async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    await expect(page.locator("main")).toBeVisible();

    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto("/");

    await expect(page.locator("main")).toBeVisible();
  });
});

test.describe("Accessibility", () => {
  test("should have no accessibility violations on homepage", async ({
    page,
  }) => {
    await page.goto("/");

    // Check for basic accessibility
    // Images should have alt text
    const images = page.locator("img");
    const imageCount = await images.count();

    for (let i = 0; i < imageCount; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute("alt");
      expect(alt).not.toBeNull();
    }

    // Buttons should have accessible names
    const buttons = page.locator("button");
    const buttonCount = await buttons.count();

    for (let i = 0; i < buttonCount; i++) {
      const button = buttons.nth(i);
      const name = await button.getAttribute("aria-label");
      const text = await button.textContent();
      expect(name || text).toBeTruthy();
    }
  });
});
