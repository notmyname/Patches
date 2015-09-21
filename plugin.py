###
# Copyright (c) 2014, John Dickinson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import re

'''
Tool to generate gerrit review URLs
'''

patch_re = r'.*?(?:patch\s+){1}(\d+).*?'
patch_regex = re.compile(patch_re)

patch_re2 = r'Console logs not available after .*? (\d+),\d+,.*?'
patch_regex2 = re.compile(patch_re2)


class Patches(callbacks.Plugin):
    """Patches is a bot that takes a patch number and makes a URL
    in the OpenStack gerrit review system.
    Patches accepts patches at https://github.com/notmyname/Patches/
    """
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Patches, self)
        self.__parent.__init__(irc)

    def testpatch(self, irc, msg, args):
        '''
        Tests that the plugin is working.
        '''
        irc.reply('testpatch command response')
    testpatch = wrap(testpatch)

    def _p(self, irc, msg, args, patch_number):
        '''<patch number>

        Generates a review.openstack.org URL to <patch number>.
        '''
        irc.reply('https://review.openstack.org/#/c/%d/' % patch_number)
    p = wrap(_p, ['int'])
    patch = wrap(_p, ['int'])

    def _foo(self, irc, msg, args, rest_of_message):
        '''
        '''
        response = 'msg: %r; args: %r; rest: %r' % (msg, args, rest_of_message)
        irc.reply(response)
    foo = wrap(_foo, [many('anything')])

    def doPrivmsg(self, irc, msg):
        channel = msg.args[0]
        match = patch_regex.findall(msg.args[1])
        for thing in match:
            self._p(irc, msg, None, int(thing))
        match2 = patch_regex2.findall(msg.args[1])
        for thing in match2:
            self._p(irc, msg, None, int(thing))

Class = Patches


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
