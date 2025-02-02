from typing import Literal, Optional, Union

from playwright.sync_api import (
    Browser,
    BrowserContext,
    ElementHandle,
    Locator,
    Page,
    Playwright,
)

from ._browser_engines import BrowserEngine

__version__ = "2.1.0"
version_info = [int(x) for x in __version__.split(".")]


def configure(**kwargs) -> None:
    """
    May be called before any other method to configure the browser settings.

    Calling this method is optional (if not called a default configuration will
    be used -- note that calling this method after the browser is already
    initialized will have no effect).

    Args:
        browser_engine: Browser engine which should be used (default: Chromium)
        headless: If set to False the browser UI will be shown. If set to True
            the browser UI will be kept hidden. If unset or set to None it'll
            show the browser UI only if a debugger is detected.
        slowmo: Run interactions in slow motion.
        screenshot: Whether to automatically capture a screenshot after each task.
            Options are `on`, `off`, and `only-on-failure` (default).
        viewport_size: Size to be set for the viewport. Specified as tuple(width, height).

    Note:
        See also: `robocorp.browser.configure_context` to change other
        arguments related to the browser context creation.
    """  # noqa
    from ._browser_context import _browser_config

    config = _browser_config()

    for key, value in kwargs.items():
        if key == "viewport_size":
            width, height = value
            configure_context(viewport={"width": width, "height": height})
            continue

        if not hasattr(config, key):
            raise ValueError(f"Invalid configuration: {key}.")
        setattr(config, key, value)


def configure_context(**kwargs) -> None:
    """
    While the most common configurations may be configured through `configure`,
    not all arguments passed to `playwright.Browser.new_context` are covered.

    For cases where different context keyword arguments are needed it's possible
    to use this method to customize the keyword arguments passed to
    `playwright.Browser.new_context`.

    Example:
        ```python
        from robocorp import browser
        browser.configure_context(ignore_https_errors = True)
        ```

    Note:
        The changes done persist through the full session, so, new tasks which
        create a browser context will also get the configuration changes.
        If the change should not be used across tasks it's possible
        to call `robocorp.browser.context(...)` with the required arguments
        directly.
    """
    from . import _browser_context

    browser_context_kwargs = _browser_context.browser_context_kwargs()
    browser_context_kwargs.update(kwargs)


def page() -> Page:
    """
    Provides a managed instance of the browser page to interact with.

    Returns:
        The browser page to interact with.

        Note that after a page is created, the same page is returned until the
        current task finishes or the page is closed.

        If a new page is required without closing the current page use:

        ```python
        from robocorp import browser
        page = browser.context().new_page()
        ```
    """
    from . import _browser_context

    return _browser_context.page()


def browser() -> Browser:
    """
    Provides a managed instance of the browser to interact with.

    Returns:
        The browser which should be interacted with.

        If no browser is created yet one is created and the same one
        is returned on new invocations.

        To customize the browser use the `configure` method (prior
        to calling this method).

        Note that the returned browser must not be closed. It will be
        automatically closed when the task run session finishes.
    """
    from . import _browser_context

    return _browser_context.browser()


def playwright() -> Playwright:
    """
    Provides a managed instance of playwright to interact with.

    Returns:
        The playwright instance to interact with.

        If no playwright instance is created yet one is created and the same one
        is returned on new invocations.

        To customize it use the `configure` method (prior
        to calling this method).

        Note that the returned instance must not be closed. It will be
        automatically closed when the task run session finishes.
    """
    from . import _browser_context

    return _browser_context.playwright()


def context(**kwargs) -> BrowserContext:
    """
    Provides a managed instance of the browser context to interact with.

    Returns:
        The browser context instance to interact with.

        If no browser context instance is created yet one is created and the
        same one is returned on new invocations.

        Note that the returned instance must not be closed. It will be
        automatically closed when the task run session finishes.

    Note:
        If the context is not created it's possible to customize the context
        arguments through the kwargs provided, by using the `configure(...)`
        method or by editing the `configure_context(...)` returned dict.

        If the context was already previously created the **kwargs passed will
        be ignored.
    """
    from . import _browser_context

    return _browser_context.context(**kwargs)


def goto(url: str) -> Page:
    """
    Changes the url of the current page (creating a page if needed).

    Args:
        url: Navigates to the provided URL.

    Returns:
        The page instance managed by the robocorp.tasks framework
        (it will be automatically closed when the task finishes).
    """
    p = page()
    p.goto(url)
    return p


def screenshot(
    element: Optional[Union[Page, ElementHandle, Locator]] = None,
    timeout: int = 5000,
    image_type: Literal["png", "jpeg"] = "png",
    log_level: Literal["INFO", "WARN", "ERROR"] = "INFO",
) -> bytes:
    """
    Takes a screenshot of the given page/element/locator and saves it to the
    log. If no element is provided the screenshot will target the current page.

    Note: the element.screenshot can be used if the screenshot is not expected
    to be added to the log.

    Args:
        element: The page/element/locator which should have its screenshot taken. If not
        given the managed page instance will be used.

    Returns:
        The bytes from the screenshot.
    """
    import base64

    from robocorp import log

    if element is None:
        from . import _browser_context

        element = _browser_context.page()

    with log.suppress():
        # Suppress log because we don't want the bytes to appear at
        # the screenshot and then as the final html.
        in_bytes = element.screenshot(timeout=timeout, type=image_type)
        in_base64 = base64.b64encode(in_bytes).decode("ascii")

    log.html(
        f'<img src="data:image/{image_type};base64,{in_base64}"/>', level=log_level
    )

    with log.suppress():
        return in_bytes


def install(browser_engine: BrowserEngine):
    """
    Downloads and installs the given browser engine.

    Note: Google Chrome or Microsoft Edge installations will be installed
    at the default global location of your operating system overriding your
    current browser installation.

    Args:
        browser_engine: Browser engine which should be installed
    """
    from . import _browser_engines

    _browser_engines.install_browser(browser_engine, force=False)


__all__ = [
    "configure",
    "configure_context",
    "page",
    "browser",
    "playwright",
    "context",
    "goto",
    "screenshot",
    "install",
    "BrowserEngine",
]
