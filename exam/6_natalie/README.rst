***********************
The Portmanteau Problem
***********************

This problem is based on the material presented in unit 6.


Overview
========

A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'.  You will write a function to
find the 'best' portmanteau word from a list of dictionary words.
Because 'portmanteau' is so easy to misspell, we will call our
function 'natalie' instead::

    natalie(['word', ...]) == 'portmanteauword'

Rules
=====

A portmanteau must be composed of three non-empty pieces, 
(start + mid + end), where both (start + mid) and (mid + end)
are among the list of words passed in.  

For example, 'adolescented' comes from 'adolescent' and 'scented'::

    adole + scent
            scent + ed
    adole + scent + ed
    START + MID   + END

A portmanteau must be composed of two different words (not the same 
word twice).

That defines an allowable combination, but which is best? Intuitively,
a longer word is better, and a word is well-balanced if the mid is
about half the total length while start and end are about 1/4 each.

To make that specific, the score for a word w is the number of letters
in w minus the difference between the actual and ideal lengths of
start, mid, and end. 

For the example word w = (adole + scent + ed), the start, mid, and 
end lengths are 5, 5, and 2 respectively, and the total length is 12.  

The ideal start, mid, end lengths are 12/4, 12/2, 12/4 = 3, 6, 3::
    
    W = "adolescented"
    A = "adole"         # start
    B = "scent"         # mid
    C = "ed"            # end

    w = len(W)          # 12
    a = len(A)          # 5
    b = len(B)          # 5
    c = len(C)          # 2

     w = a + b + c
    12 = 5 + 5 + 2

    q = w / 4           # 3 (preferred length of start)
    r = w / 2           # 6 (preferred length of mid)
    s = w / 4           # 6 (preferred length of end)
    
     w - abs(a-q) - abs(b-r) - abs(c-s)
    12 - abs(5-3) - abs(5-6) - abs(2-3)
    12 - 2        - 1        - 1

So the final score for the word "adolescented" is 8::

    12 - abs(5-(12/4)) - abs(5-(12/2)) - abs(2-(12/4))
    12 - (2 - 1 - 1)  ==  12 - 4  ==  8 


The output of natalie(words) should be the best portmanteau, 
or None if there is none. 


Notes
=====

1. I got the idea for this question from Darius Bacon.  

2. In real life, many portmanteaux omit letters, for example 
   'smoke' + 'fog' = 'smog'; we aren't considering those.

3. The word 'portmanteau' is itself a portmanteau; it comes
   from the French "porter" (to carry) + "manteau" (cloak), and in
   English meant "suitcase" in 1871 when Lewis Carroll used it in
   'Through the Looking Glass' to mean two words packed into one. 

4. The rules for 'best' are certainly subjective, and certainly
   should depend on more things than just letter length.  In addition 
   to programming the solution described here, you are welcome to explore
   your own definition of best, and use your own word lists to come up
   with interesting new results.  Post your best ones in the discussion
   forum. 

5. The test examples will involve no more than a dozen or so
   input words. But you could implement a method that is efficient 
   with a larger list of words.  

6. The submission system should accept your program if it gives any
   solutions that have equally good scores as the ones shown in the 
   assertions.  You might want to define your own way of determining 
   which portmanteau is the best among equal-scoring candidates (based 
   on length, for example, or however else you want to choose), but all 
   solutions that have a score equal to best score are acceptable; your 
   function should return any one of them (not a collection of them).
