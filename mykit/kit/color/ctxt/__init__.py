"""
this is the next generation of mykit.kit.color.Colored (mykit-9 ver),
with bugs fixed and even better.
"""
import os as _os
import re as _re
import sys as _sys
from typing import (
    Optional as _Optional,
)

from mykit.kit.color import (
    Hex as _Hex,
    hex_to_rgb as _hex_to_rgb
)
from mykit.kit.str_ops.lcut import lcut as _lcut
from mykit.kit.str_ops.rcut import rcut as _rcut


## The reset code to end the coloring
_RESET = '\033[0m'  # note, "\033" is the same as "\x1b"


class _Runtime:

    ## to make ctxt work inside Windows Command Prompt
    win_init = False


## Birthdate: Oct 6, 2023
def ctxt(text:str, foreground:str=_Hex.LAVENDER_GRAY, background:_Optional[str]=None) -> str:
    """
    Colored Text (ctxt)

    ## Params
    - `text`: The input string, don't worry, `ctxt` will do `text=str(text)` later.
    - `foreground`: in hex format.
    - `background`: in hex format. If `None`, the default terminal background color will be used.

    ## Demo

    ## Docs
    - The text (or parts of the text) that have already been colored cannot have their
        color changed. P.S. I'm not really sure about this one actually.
    """
    
    ## Windows users
    if _sys.platform.lower() == 'win32':
        if not _Runtime.win_init:
            _os.system('color')
            _Runtime.win_init = True

    ## Guard
    text = str(text)

    fg_r, fg_g, fg_b = _hex_to_rgb(foreground)

    header = '\033[' + f'38;2;{fg_r};{fg_g};{fg_b}'

    ## Background
    if background is not None:
        bg_r, bg_g, bg_b = _hex_to_rgb(background)
        header += f';48;2;{bg_r};{bg_g};{bg_b}'
    
    header += 'm'

    """=DOCS=
    color-in-color mechanism
    ========================

    the goals: make it color-in-color properly + no redundancies

    - since all text output from ctxt will have the format H-T-R, where H is the header, T is text, and R is the reset code.

    let's start easy, for a single-color text, it's clear that it's just HTR.

    now, let's add that with plain text, and it becomes HTR_T.

    next, let's add it again with a single-colored text again, and now it becomes HTR_T_HTR.

    now, here is the color-in-color problem. if we just literally put HTR_T_HTR into ctxt, the output would look like H_HTR_T_HTR_R.

    i'm sorry, it's hard to tell which color is which, but let's focus on the order of H and R.

    if we look at H_HTR_T_HTR_R, the middle text (the one that has no color) still has no color (which it's actually should).

    before continuing, here are the things that i observed from a few experiments with it:
    - if there are 2 H's next to each other, the rightmost H will only be used. for example, H1_H2_T, then T will be colored H2.
        also true, if there are 3, 4, or more Hs.
    - all the texts at the right of an H will share the H color. for example, H_T1_T2_T3, all the T1, T2, T3 will have the same color.
    - then, we could say that in order to change/stop the color, we should have either a new H or use R to change or stop the coloring.
    
    
    back again with HTR_T_HTR, one way we could do is H_HTR_HTR_HTR_R. but this is really ridiculous in my mind.
    another way is H_HTRH_T_HTRH_R. here we subtitute all Rs in HTR_T_HTR with RH (R -> RH).

    now, the good news is RH is actually the same as just H. for example, RH_T is the same as H_T.
    also, HR is the same as just R. for example, T_HR is the same as T_R, which is also the same as just T.

    okay, but this is the ideal, HTR_T_HTR -> HT_HT_HTR  (we apply a color to HTR_T_HTR, so it becomes HT_HT_HTR).
    with this version, all H and R are truly doing their job, and there should be no redundancies.

    i have no idea how, but let's list all the ideal cases:
    - HTR_T_HTR -> HT_HT_HTR
    - HTR_T_HTR_T -> HT_HT_HT_HTR
    - T_HTR_T_HTR_T -> HT_HT_HT_HT_HTR
    - H1T_H2TR_T_H2T_H1TR -> H1T_H2T_H3T_H2T_H1TR

    well, it seems there should be only 1 R for each case, which is just at the end.
    or in more proper words, all colored text output from ctxt will just have one R, which is at the end.

    let's back with the simple T, it gonna become HTR, HTR_T is gonna become HT_HTR. T_HTR -> HT_HTR. HTR_T_HTR -> HT_HT_HTR

    okay, hoping that's all

    update: turns out the sequence can't be HT_HT_HT_... because the background is optional.
    if no background at all, it's fine, but if there's a background, the background won't change after the next H.
    the R terminates both foreground and background if two Hs are next to each other, and only the first one has a background.
    the next T will also share the same background. for example, H1T1_H2T2, if H1 has a background but H2 does not,
    T1 and T2 will have the same background (which T2 shouldnt).

    
    so then, the sequence should be HTR_HTR_HTR_ and so on. it's redundant for no BGs, but yeah :)) hopefully soon i could make it better.

    update (final): okay i think im confidently believe that HTR_HTR_HTR... is the safest and ideal sequence for it
    """

    ## <color-in-color>

    ## If the ending is _RESET, remove that so there would be no TR -> TRH -> TRHR (which we expect should be just TR).
    # if text.endswith(_RESET):
    #     text = _rcut(text, _RESET)  # dev-docs: after #1, these lines no longer needed

    ## after #2, it needs these:
    if text.endswith(_RESET):
        text = _rcut(text, _RESET)

    ## Color the uncolored (replace all R with RH)
    # if _RESET in text:
    #     text = text.replace(_RESET, _RESET + header)
    ## vvvvvvvvvvvvvvvvv dev-docs: let's say it's HTR_T_HTR. initially, it becomes HTR_HT_HTR,
    ##                             which is a problem where the last 'T' will have the same background
    ##                             if the middle 'H' has a background while the last 'H' does not.
    ##                             so, it should be HTR_T_HTR -> HT_RHT_RHTR
    # if _RESET in text:
    #     text = text.replace(_RESET, _RESET + header)
    # if '\033[38;2' in text:
    #     text = text.replace(_RESET, _RESET + header)
    ## vvv #1 vvvvvvvvvvvvvvvvv dev-docs: above method will replace all the H and R which is redundant.
    text = _re.sub(r'\033\[0m(?!\033\[38;2)', _RESET+header, text)        # Replace all R (that are not followed by H) with RH
    text = _re.sub(r'(?<!\033\[0m)\033\[38;2', _RESET+'\033[38;2', text)  # Replace all H (that are not preceded by R) with RH


    ## ~~to avoid double coloring (HRH), check if the beginning of `text` is~~
    ## to avoid double coloring (HH), check if the beginning of `text` is
    ## already colored. If it is, no header needs to be inserted at the beginning.
    # if text.startswith(_RESET):
    # if text.startswith('\033['):
    #     header = ''
    ## vvvvvvvvvvvvvvvv dev-docs: after previous step, the begining wil start with _RESET
    # if text.startswith(_RESET):
    #     header = ''  # dev-docs: after #1, these lines no longer needed

    ## after #1, need these:
    # if text.startswith('\033[38;2'):  # starts with H
    #     the_header = ''
    # else:
    #     the_header = header
    # if text.endswith(_RESET):
    #     the_ending = ''
    # else:
    #     the_ending = _RESET
    ## vvv #2 vvvvvvvvv: dev-docs: initially, i thought the final would look like HTR_HTR_HTR, but it turns out to be RHTR_HTR_HTRH.
    ##                             it's fine to just make it HRHTR_HTR_HTRHR, but it's redundant.
    if text.startswith(_RESET):
        text = _lcut(text, _RESET)
        the_header = ''
    else:
        the_header = header

    ## </color-in-color>

    # return _RESET+header + text + _RESET  # should we go with this? im not sure, but i think the R at the end alone should be enough
    # return header + text + _RESET  # dev-docs: after #1, this line is not the right one
    # return text
    ## vvvvv dev-docs: silly, but we back with this again
    # return the_header + text + the_ending
    ## vvv after #2
    return the_header + text + _RESET
