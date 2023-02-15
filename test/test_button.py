"""Test that src/components/button.py works correctly"""

import pytest

from tui.components.button import Button

pytest_plugins = ('pytest_asyncio')


@pytest.mark.asyncio
async def test_button_on_click_no_parameters():
    """Test that on_click event executes a callback function with one
    parameter"""
    btn = Button()

    @btn.on_click()
    def do_nothing() -> None:
        raise AssertionError

    # an exception will be raised if do_nothing is called
    with pytest.raises(AssertionError):
        await btn.click_signal()


@pytest.mark.asyncio
async def test_button_on_click():
    """Test that on_click event executes a callback function with one
    parameter"""
    btn = Button()

    @btn.on_click(button=btn)
    def change_btn_text(button: Button) -> None:
        button.text = '1'

    await btn.click_signal()
    assert btn.text == '1'


@pytest.mark.asyncio
async def test_button_on_click_multiple_parameters():
    """Test that on_click event executes callback function with multiple
    parameters"""
    btn = Button()

    @btn.on_click(button=btn, char='a')
    def change_btn_text(button: Button, char: str) -> None:
        button.text = char

    await btn.click_signal()
    assert btn.text == 'a'


@pytest.mark.asyncio
async def test_button_on_click_multiple_decorators_multiple_parameters():
    """Test that on_click event executes 2 callback functions when there are
    2 decorators, each taking multiple parameters"""
    btn1 = Button()
    btn2 = Button()

    # @btn1.on_click(button=btn1, char='1')
    # @btn1.on_click(button=btn2, char='2')
    def change_btn_text(button: Button, char: str) -> None:
        button.text = char

    btn1.on_click(button=btn1, char='1')(change_btn_text)
    btn1.on_click(button=btn2, char='2')(change_btn_text)

    await btn1.click_signal()
    assert btn1.text == '1' and btn2.text == '2'
