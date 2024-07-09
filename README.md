Start the game using:

    python3 main.py

Use 'A' and 'D' to move left or right

Use 'Spacebar' to release ball from paddle

Use 'P' to pause the game

Use 'Q' to quit the game

Use 'N' to skip to next level

Use 'U' to shoot bullets if power up is active

Falling bricks is activated after 200 time units after entering new level

The bricks have 5 colors: light_green for strength 1, blue for strength 2, red for strength 3, and magenta for indestructible bricks and the rainbow brick which cycles through each of the strengths(1-3) until it is hit for the first time after which it will keep the strength of the brick at the time of collision

Power ups now have initial velocity as same as the ball which hit the brick, also gravity is applied on it which leads to acceleration of power up as it goes down

Boss drops a bomb about every 50 time units since last bomb was dropped, the bomb is green in color

Shooting paddle power up lasts for about 100 time units, and we can shoot bullets about once every 10 time units, the bullets are cyan in color.

Number of bricks generated are constant depending on terminal size, but strength and whether it is indestructible is chosen randomly.

The Game has 7 powerups which appear as Light black squares with a number in them, depending on the type of powerup. The number in the square go from 1 to 7, and correspond to:

1: Increase paddle length by 3 characters worth of space for 100 time units,where time is the time as shown on screen

2: Same as 1, but paddle length decreases by 3

3: A new ball is created for every current ball, velocity of new ball is complete opposite of original

4: Increase ball speed by 1 character worth of space per time unit, for 100 time units

5: All current Balls instantly destroys all bricks(even indestructible ones) and doesn't go through elastic collision and instead just passes straight through, for 100 time units

6: Whenever ball touches paddle, paddle automactically grabs the ball, valid for 100 time units and once used cant be used again even if 100 time units not passed

7: Player can shoot bullets from the paddle by using the button 'U' for 100 time units with a 10 time unit gap between each fire

Score is the number of bricks destroyed plus extra score for beating the boss

If ball hits closer to middle of panel then ball will have more vertical velocity, if it hits near edge then ball will have more horizontal velocity

Probability of a brick being indestructible is about 10% and probability of some powerup being released on destruction of brick is 30% with equal probability of it being any of the 7 powerups.

Also I have made it so that 2nd defense of UFO is only activated if all bricks of first layer are destroyed, since I was not sure how it was to be implemented. Changing this to do otherwise will also work fine

The defense only gets formed after the ball in lower in the y axis than where bricks are to be formed so as to ensure the bricks dont cause the ball to bounce back to the ufo and creating a feed-back loop