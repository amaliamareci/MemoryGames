from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import NumberSequenceGame, ColorPairsGame, DirectionalMemoryGame

def home(request):
    """Home page showing available games"""
    return render(request, 'game/home.html')

def number_sequence(request):
    """Number sequence memory game"""
    # Get level and card count from session, or use defaults
    level = request.session.get('level', 1)
    card_count = request.session.get('card_count', 4)
    
    # Clean up old games
    NumberSequenceGame.objects.all().delete()
    
    # Create new game with current level settings
    game = NumberSequenceGame.objects.create(
        numbers_sequence=[],
        current_level=level,
        card_count=card_count
    )
    game.generate_sequence()
    return render(request, 'game/number_sequence.html', {'game': game})

@require_http_methods(['POST'])
def check_sequence(request, game_id):
    game = NumberSequenceGame.objects.get(id=game_id)
    clicked_number = int(request.POST.get('number'))
    current_index = int(request.POST.get('current_index', 0))
    
    # We expect numbers to be clicked in order: 1, 2, 3, ...
    expected_number = current_index + 1
    
    if clicked_number != expected_number:
        # Wrong sequence - reset to 4 cards
        request.session['level'] = 1
        request.session['card_count'] = 4
        return HttpResponse(
            '<div class="text-center mb-4">'
            '<h3 class="text-xl font-bold text-red-600">Wrong sequence!</h3>'
            '<p>Starting over with 4 cards...</p></div>'
            '<script>'
            'setTimeout(function() {'
            '  window.location.href = "/number-sequence/";'
            '}, 1500);'
            '</script>'
        )

    # If we reach here, the correct number was clicked
    if current_index == len(game.numbers_sequence) - 1:
        # Completed the sequence
        if game.card_count >= 10:
            game.is_completed = True
            game.save()
            # Reset session for next game but don't redirect automatically
            request.session['level'] = 1
            request.session['card_count'] = 4
            return HttpResponse(
                '<div class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" id="winner-screen">'
                '<div class="text-center relative z-10">'
                '<h2 class="text-6xl font-bold text-yellow-400 mb-8 animate-bounce">🎉 WINNER! 🎉</h2>'
                '<p class="text-2xl text-white mb-8">Congratulations! You\'ve mastered all levels!</p>'
                '<button onclick="window.location.href=\'/number-sequence/\'" '
                'class="bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-3 px-6 rounded-lg '
                'transform transition hover:scale-110 text-xl">'
                'Play Again</button>'
                '</div>'
                + FIREWORKS_CSS +
                '<div class="firework"></div>'
                '<div class="firework"></div>'
                '<div class="firework"></div>'
                '</div>'
            )
        
        # Store next level's settings in session
        next_level = game.current_level + 1
        next_card_count = min(game.card_count + 2, 10)
        request.session['level'] = next_level
        request.session['card_count'] = next_card_count
        
        return HttpResponse(
            '<div class="text-center mb-4">'
            '<h3 class="text-xl font-bold text-green-600">Level Complete!</h3>'
            f'<p>Moving to Level {next_level} with {next_card_count} cards...</p></div>'
            '<script>'
            'setTimeout(function() {'
            '  window.location.href = "/number-sequence/";'
            '}, 1500);'
            '</script>'
        )
    
    # Return the next index
    return HttpResponse(str(current_index + 1))

# Move the fireworks CSS to a constant to keep the code cleaner
FIREWORKS_CSS = '''
<style>
@keyframes firework {
    0% { transform: translate(var(--x), var(--initialY)); width: var(--initialSize); opacity: 1; }
    50% { width: 0.5vmin; opacity: 1; }
    100% { width: var(--finalSize); opacity: 0; }
}
.firework,
.firework::before,
.firework::after {
    --initialSize: 0.5vmin;
    --finalSize: 45vmin;
    --particleSize: 0.2vmin;
    --color1: yellow;
    --color2: khaki;
    --color3: white;
    --color4: lime;
    --color5: gold;
    --color6: mediumseagreen;
    --y: -30vmin;
    --x: -50%;
    --initialY: 60vmin;
    content: "";
    animation: firework 2s infinite;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, var(--y));
    width: var(--initialSize);
    aspect-ratio: 1;
    background: 
        radial-gradient(circle, var(--color1) var(--particleSize), #0000 0) 50% 0%,
        radial-gradient(circle, var(--color2) var(--particleSize), #0000 0) 100% 50%,
        radial-gradient(circle, var(--color3) var(--particleSize), #0000 0) 50% 100%,
        radial-gradient(circle, var(--color4) var(--particleSize), #0000 0) 0% 50%,
        radial-gradient(circle, var(--color5) var(--particleSize), #0000 0) 80% 90%,
        radial-gradient(circle, var(--color6) var(--particleSize), #0000 0) 95% 90%;
    background-size: var(--initialSize) var(--initialSize);
    background-repeat: no-repeat;
}
.firework::before {
    --x: -50%;
    --y: -50%;
    --initialY: -50%;
    transform: translate(-50%, -50%) rotate(40deg) scale(1.3) rotateY(40deg);
}
.firework::after {
    --x: -50%;
    --y: -50%;
    --initialY: -50%;
    transform: translate(-50%, -50%) rotate(170deg) scale(1.15) rotateY(-30deg);
}
.firework:nth-child(2) {
    --x: 30vmin;
}
.firework:nth-child(2),
.firework:nth-child(2)::before,
.firework:nth-child(2)::after {
    --color1: pink;
    --color2: violet;
    --color3: fuchsia;
    --color4: orchid;
    --color5: plum;
    --color6: lavender;
    --finalSize: 40vmin;
}
.firework:nth-child(3) {
    --x: -30vmin;
    --y: -10vmin;
}
.firework:nth-child(3),
.firework:nth-child(3)::before,
.firework:nth-child(3)::after {
    --color1: cyan;
    --color2: lightcyan;
    --color3: lightblue;
    --color4: PaleTurquoise;
    --color5: SkyBlue;
    --color6: lavender;
    --finalSize: 35vmin;
}
</style>
'''

@require_http_methods(['POST'])
def reset_game(request, game_id):
    # Reset session values
    request.session['level'] = 1
    request.session['card_count'] = 4
    return redirect('/number-sequence/')

def color_pairs(request):
    """Color pairs memory game"""
    # Get level and card count from session, or use defaults
    level = request.session.get('pairs_level', 1)
    card_count = request.session.get('pairs_card_count', 4)
    
    # Clean up old games
    ColorPairsGame.objects.all().delete()
    
    # Create new game with current level settings
    game = ColorPairsGame.objects.create(
        current_level=level,
        card_count=card_count
    )
    game.generate_sequence()
    return render(request, 'game/color_pairs.html', {'game': game})

@require_http_methods(['POST'])
def check_pairs(request, game_id):
    game = ColorPairsGame.objects.get(id=game_id)
    
    if game.card_count >= 10:  # Final level completed (changed from 8 to 10)
        game.is_completed = True
        game.save()
        # Reset session for next game but don't redirect automatically
        request.session['pairs_level'] = 1
        request.session['pairs_card_count'] = 4
        return HttpResponse(
            '<div class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" id="winner-screen">'
            '<div class="text-center relative z-10">'
            '<h2 class="text-6xl font-bold text-yellow-400 mb-8 animate-bounce">🎉 WINNER! 🎉</h2>'
            '<p class="text-2xl text-white mb-8">Congratulations! You\'ve mastered all levels!</p>'
            '<button onclick="window.location.href=\'/color-pairs/\'" '
            'class="bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-3 px-6 rounded-lg '
            'transform transition hover:scale-110 text-xl">'
            'Play Again</button>'
            '</div>'
            + FIREWORKS_CSS +
            '<div class="firework"></div>'
            '<div class="firework"></div>'
            '<div class="firework"></div>'
            '</div>'
        )
    
    # Store next level's settings in session
    next_level = game.current_level + 1
    next_card_count = min(game.card_count + 2, 10)  # Updated to support up to 10 cards
    request.session['pairs_level'] = next_level
    request.session['pairs_card_count'] = next_card_count
    
    game.increase_difficulty()
    return HttpResponse(
        '<div class="text-center mb-4">'
        '<h3 class="text-xl font-bold text-green-600">Level Complete!</h3>'
        f'<p>Moving to Level {next_level} with {next_card_count} cards ({next_card_count//2} pairs)...</p></div>'
    )

@require_http_methods(['POST'])
def reset_pairs(request, game_id):
    # Reset session values
    request.session['pairs_level'] = 1
    request.session['pairs_card_count'] = 4
    return redirect('/color-pairs/')

def directional_memory(request):
    """Directional memory game"""
    # Get level and sequence length from session, or use defaults
    level = request.session.get('direction_level', 1)
    sequence_length = request.session.get('sequence_length', 3)
    
    # Clean up old games
    DirectionalMemoryGame.objects.all().delete()
    
    # Create new game with current level settings
    game = DirectionalMemoryGame.objects.create(
        current_level=level,
        sequence_length=sequence_length
    )
    game.generate_sequence()
    return render(request, 'game/directional_memory.html', {'game': game})

@require_http_methods(['POST'])
def check_direction(request, game_id):
    game = DirectionalMemoryGame.objects.get(id=game_id)
    clicked_arrow = request.POST.get('arrow')
    current_index = int(request.POST.get('current_index', 0))
    
    # Check if the clicked arrow matches the expected arrow in the sequence
    if clicked_arrow != game.arrow_sequence[current_index]:
        # Wrong sequence - reset to 3 arrows
        request.session['direction_level'] = 1
        request.session['sequence_length'] = 3
        return HttpResponse(
            '<div class="text-center mb-4">'
            '<h3 class="text-xl font-bold text-red-600">Wrong sequence!</h3>'
            '<p>Starting over with 3 arrows...</p></div>'
        )

    # If we reach here, the correct arrow was clicked
    if current_index == len(game.arrow_sequence) - 1:
        # Completed the sequence
        if game.sequence_length >= 5:  # Final level completed
            game.is_completed = True
            game.save()
            # Reset session for next game but don't redirect automatically
            request.session['direction_level'] = 1
            request.session['sequence_length'] = 3
            return HttpResponse(
                '<div class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" id="winner-screen">'
                '<div class="text-center relative z-10">'
                '<h2 class="text-6xl font-bold text-yellow-400 mb-8 animate-bounce">🎉 WINNER! 🎉</h2>'
                '<p class="text-2xl text-white mb-8">Congratulations! You\'ve mastered all levels!</p>'
                '<button onclick="window.location.href=\'/directional-memory/\'" '
                'class="bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-3 px-6 rounded-lg '
                'transform transition hover:scale-110 text-xl">'
                'Play Again</button>'
                '</div>'
                + FIREWORKS_CSS +
                '<div class="firework"></div>'
                '<div class="firework"></div>'
                '<div class="firework"></div>'
                '</div>'
            )
        
        # Store next level's settings in session
        next_level = game.current_level + 1
        next_sequence_length = min(game.sequence_length + 1, 5)
        request.session['direction_level'] = next_level
        request.session['sequence_length'] = next_sequence_length
        
        game.increase_difficulty()
        return HttpResponse(
            '<div class="text-center mb-4">'
            '<h3 class="text-xl font-bold text-green-600">Level Complete!</h3>'
            f'<p>Moving to Level {next_level} with {next_sequence_length} arrows...</p></div>'
        )
    
    # Return the next index
    return HttpResponse(str(current_index + 1))

@require_http_methods(['POST'])
def reset_direction(request, game_id):
    # Reset session values
    request.session['direction_level'] = 1
    request.session['sequence_length'] = 3
    return redirect('/directional-memory/')
