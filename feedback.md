**Grade: 84.5**

# Tutor Feedback

## Exercise 1: Variable Selection Heuristics (10/10)

### MD Heuristic (4/4)

### MRV Heuristic (4/4)

### MD-MRV Heuristic (1/1)

### MRV-MD Heuristic (1/1)

## Exercise 2: Value Selection Heuristics (5/5)

## Exercise 3: Forward Checking (10/10)

## Exercise 4: AC-3 (20/25)

* -2 Copying `current_domains` for all variables is potentially copying
  unnecessary information. Consider the case where your algorithm is provided a
  variable (in `var`) and the current problem is already arc consistent.
* -2 You have a lot of code duplication here. The only difference between AC-3
  with and without value for `var` is how the queue is initialised - you can
  easily factor that out.
* -1 Your pruning is not quite right: it does not include all variable, value
  pairs that can be pruned in e.g. `8_queens`.

## Exercise 5: N-ary Compiler (16/20)

* -2 Your compiler sometimes converts satisfiable CSPs into unsatisfiable ones
  e.g. `test_sat_2.csp`. This is because you have spaces in your variable names,
  which causes syntax issues.
* -2 Your code is quite clean and concise, but you need to add some more
  comments.
* Otherwise, looks good!

## Exercise 6: Wumpus Where Are You? (23.5/30)

### Code (20/20)

* Your implementation found all safe, unsafe, trivial, and uncertain paths in
  our tests, excellent work!
* In terms of code quality, your commenting is very good, well done! My only
  suggestion is that you could try to split up your code into some more
  functions.

### Report (3.5/10)

* -0.5 In the high level description of your approach: 
  * You're missing a bit of detail, e.g. what are the domains of your variables?
  * A diagram would help in making your description easier to understand.
  * It seems like there's a typo in your discussion of "output files" - you say
    that for both CSPs you fix the next location of the agent to be pit or
    wumpus.
* That being said, your level of detail is quite good, so just fill in the gaps
  and edit it a bit.
* -6 No experiment or conclusion. It's a shame that you didn't have time to get
  this done, since your CSP generator works quite well! Make sure you leave
  yourself enough time to run experiments in future assignments where the
  results are worth more.