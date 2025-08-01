from typing import AsyncGenerator, Generator, List, no_type_check

import pytest
import pytest_asyncio
from playwright.async_api import Page as AsyncPage
from playwright.async_api import async_playwright
from playwright.sync_api import Page as SyncPage
from playwright.sync_api import sync_playwright

from cdp_patches.input import AsyncInput, SyncInput

from .server import Server, test_server

flags: List[str] = [
    "--incognito",
    "--accept-lang=en-US",
    "--lang=en-US",
    "--no-pings",
    "--mute-audio",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-cloud-import",
    "--disable-gesture-typing",
    "--disable-offer-store-unmasked-wallet-cards",
    "--disable-offer-upload-credit-cards",
    "--disable-print-preview",
    "--disable-voice-input",
    "--disable-wake-on-wifi",
    "--disable-cookie-encryption",
    "--ignore-gpu-blocklist",
    "--enable-async-dns",
    "--enable-simple-cache-backend",
    "--enable-tcp-fast-open",
    "--prerender-from-omnibox=disabled",
    "--enable-web-bluetooth",
    "--disable-features=AudioServiceOutOfProcess,IsolateOrigins,site-per-process,TranslateUI,BlinkGenPropertyTrees",
    "--aggressive-cache-discard",
    "--disable-extensions",
    "--disable-ipc-flooding-protection",
    "--disable-blink-features=AutomationControlled",
    "--test-type",
    "--enable-features=NetworkService,NetworkServiceInProcess,TrustTokens,TrustTokensAlwaysAllowIssuance",
    "--disable-component-extensions-with-background-pages",
    "--disable-default-apps",
    "--disable-breakpad",
    "--disable-component-update",
    "--disable-domain-reliability",
    "--disable-sync",
    "--disable-client-side-phishing-detection",
    "--disable-hang-monitor",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--metrics-recording-only",
    "--safebrowsing-disable-auto-update",
    "--password-store=basic",
    "--autoplay-policy=no-user-gesture-required",
    "--use-mock-keychain",
    "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
    "--disable-session-crashed-bubble",
    "--disable-crash-reporter",
    "--disable-dev-shm-usage",
    "--force-color-profile=srgb",
    "--disable-translate",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-infobars",
    "--hide-scrollbars",
    "--disable-renderer-backgrounding",
    "--font-render-hinting=none",
    "--disable-logging",
    "--enable-surface-synchronization",
    "--run-all-compositor-stages-before-draw",
    "--disable-threaded-animation",
    "--disable-threaded-scrolling",
    "--disable-checker-imaging",
    "--disable-new-content-rendering-timeout",
    "--disable-image-animation-resync",
    "--disable-partial-raster",
    "--blink-settings=primaryHoverType=2,availableHoverTypes=2," "primaryPointerType=4,availablePointerTypes=4",
    "--disable-layer-tree-host-memory-pressure",
]


@pytest_asyncio.fixture(autouse=True, scope="session")
def run_around_tests():
    test_server.start()
    yield
    test_server.stop()


# tests\conftest.py:98: error: Value of type variable "_R" of "fixture" cannot be "Generator[Server, None, None]"  [type-var]
# and I DON'T WANT TO GET INTO THAT HOLE NOW
@no_type_check
@pytest_asyncio.fixture
def server() -> Generator[Server, None, None]:
    yield test_server.server


@pytest.fixture
def sync_page() -> Generator[SyncPage, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=flags)
        context = browser.new_context(locale="en-US")
        page = context.new_page()
        page.sync_input = SyncInput(browser=context)  # type: ignore[attr-defined]

        yield page


@pytest_asyncio.fixture
async def async_page() -> AsyncGenerator[AsyncPage, None]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=flags)
        context = await browser.new_context(locale="en-US")
        page = await context.new_page()
        page.async_input = await AsyncInput(browser=context)  # type: ignore[attr-defined]
        yield page
