# switchs-card-game

Game was mostly done for fun in a matter of 2~3 hours and is not finished. It is only uploaded for learning purposes as it is no longer of any use to me. I do not intend to fix the bugs it currently contains (further explained below). I may however, help with questions regarding the code.

This is a basic Python implementation of the Switch (card game), however, with different rules. The game supports up to an unlimited number of bots. Player is always assigned to index 0, while bots receive their ID's accordingly (varies on assignment).

<hr/>
<b>Card types:</b>
	<ul>
		<li>Ace: Player gets to play whatever card he desires, regardless of what already exists on field.</li></li>
		<li>7: Refers to the "plus two" card. Placing on top of it will cause the other player to get +2 (extra, on top of what it already is).</li>
		<li>8: Player gets to play again. This cannot be an ending card.</li>
  <li>9: Cause next player to loose his turn.</li>
	</ul>
  
  <hr/>
<b>Game rules:</b>
<ul>
  <li>The deck is formed of a total of 52 cards.</li>
  <li>Each player starts with 7 cards each. A random card is drawn from deck on game start.</li>
  <li>The player player must throw a card of the same figure (symbol) or of same number (symbol does not matter in the latter).</li>
  <li>Invalid moves are not allowed. Players will be allowed to play again if move is invalid.</li>
  <li>Play may 'skip' his move at any point in time, regardless of whether he has got available moves or not (skipping gives top card from deck to player).</li>
  <li>If no cards are left in the deck, the played cards are shuffled, last card is left on top and the rest is set as the hidden deck.</li>
  <li>When a player has no cards left in his hand, the round ends.</li>
  <li>Player score equals total hand cards value (each card has got a specific value).</li>
  <li>Game ends when one of the players reaches a score of 50. Players are ordered starting from the one with less score.</li>
 </ul>

<hr/>
<b>Bugs:</b>
<ul><li>Sometimes there will be an infinite skipping loop between one player and a bot.</li>
<li>Sometimes there will be an infinite additioning loop &/ players will not be able to play a card.</li>
</ul>

Feel free to use it for learning purposes.
