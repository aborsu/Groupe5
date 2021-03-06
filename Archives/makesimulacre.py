#/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sans titre.py
#  
#  Copyright 2013 Sarah Beniamine <sarah.beniamine@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  



def main():
    instream = open("ftb_test.txt", "r", encoding = "utf8")
    outstream = open("ftb_test_accolades.txt", "w", encoding = "utf8")
    for phrase in instream:
        listph = phrase[:-1].split(" ")
        ph = [ "{"+str(num)+" "+word+"}"+word for num,word in enumerate(listph)]
        outstream.write(" ".join(ph) + "\n")

if __name__ == '__main__':
	main()

