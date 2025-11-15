import { NextResponse } from "next/server";
import puppeteer from "puppeteer-core";
import chromium from "@sparticuz/chromium";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const groupName = searchParams.get("group");

  if (!groupName) {
    return NextResponse.json({ error: "Missing group name" }, { status: 400 });
  }

  const schemaUrl = new URL("/schema", request.url);
  schemaUrl.searchParams.set("group", groupName);

  let browser;
  try {
    const executablePath = process.env.PUPPETEER_EXECUTABLE_PATH || (await chromium.executablePath());
    browser = await puppeteer.launch({
      executablePath,
      headless: true,
      args: chromium.args,
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    page.setDefaultNavigationTimeout(300000);
    page.setDefaultTimeout(300000);
    await page.goto(schemaUrl.toString(), {
      waitUntil: "networkidle0",
      timeout: 300000,
    });

    await page.waitForSelector("[data-layouts]", { timeout: 300000 });
    await page.waitForSelector("[data-settings]", { timeout: 300000 });

    const { dataLayouts, dataGroupSettings } = await page.$eval(
      "[data-layouts]",
      (el) => ({
        dataLayouts: el.getAttribute("data-layouts"),
        dataGroupSettings: el.getAttribute("data-settings"),
      })
    );

    let slides, groupSettings;
    try {
      slides = JSON.parse(dataLayouts || "[]");
    } catch (e) {
      slides = [];
    }
    try {
      groupSettings = JSON.parse(dataGroupSettings || "null");
    } catch (e) {
      groupSettings = null;
    }

    const response = {
      name: groupName,
      ordered: groupSettings?.ordered ?? false,
      slides: slides.map((slide: any) => ({
        id: slide.id,
        name: slide.name,
        description: slide.description,
        json_schema: slide.json_schema,
      })),
    };

    return NextResponse.json(response);
  } catch (err) {
    return NextResponse.json(
      { error: "Failed to fetch or parse client page" },
      { status: 500 }
    );
  } finally {
    if (browser) await browser.close();
  }
}

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
