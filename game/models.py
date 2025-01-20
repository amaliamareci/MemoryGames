from django.db import models
import random
import json

class BaseGame(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🎮')  # Emoji or icon class
    url_path = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class NumberSequenceGame(models.Model):
    name = models.CharField(max_length=100, default="Number Sequence")
    description = models.TextField(default="Memorize and click numbers in sequence")
    icon = models.CharField(max_length=50, default='🔢')
    url_path = models.CharField(max_length=100, default='number-sequence')
    created_at = models.DateTimeField(auto_now_add=True)
    current_level = models.IntegerField(default=1)
    card_count = models.IntegerField(default=4)
    numbers_sequence = models.JSONField(default=list)
    is_completed = models.BooleanField(default=False)

    def generate_sequence(self):
        numbers = list(range(1, self.card_count + 1))
        random.shuffle(numbers)
        self.numbers_sequence = numbers
        self.save()
        return numbers

    def increase_difficulty(self):
        if self.card_count < 10:
            self.card_count = min(self.card_count + 2, 10)
            self.current_level += 1
            self.generate_sequence()
            self.save()
        else:
            self.is_completed = True
            self.save()

    def reset_game(self):
        self.card_count = 4
        self.current_level = 1
        self.is_completed = False
        self.generate_sequence()
        self.save()

class ColorPairsGame(models.Model):
    name = models.CharField(max_length=100, default="Color Pairs")
    description = models.TextField(default="Find matching color pairs")
    icon = models.CharField(max_length=50, default='🎨')
    url_path = models.CharField(max_length=100, default='color-pairs')
    created_at = models.DateTimeField(auto_now_add=True)
    current_level = models.IntegerField(default=1)
    card_count = models.IntegerField(default=4)
    colors_sequence = models.JSONField(default=list)
    is_completed = models.BooleanField(default=False)

    COLORS = [
        {'name': 'green', 'hex': '#22c55e'},
        {'name': 'yellow', 'hex': '#eab308'},
        {'name': 'blue', 'hex': '#3b82f6'},
        {'name': 'red', 'hex': '#ef4444'},
        {'name': 'purple', 'hex': '#a855f7'},
        {'name': 'orange', 'hex': '#f97316'}
    ]

    def generate_sequence(self):
        # Calculate number of pairs needed
        pairs_count = self.card_count // 2
        # Select colors for this level
        level_colors = self.COLORS[:pairs_count]
        # Create pairs
        pairs = level_colors * 2
        # Shuffle the pairs
        random.shuffle(pairs)
        self.colors_sequence = pairs
        self.save()
        return pairs

    def increase_difficulty(self):
        if self.card_count < 10:  # Four levels: 4, 6, 8, and 10 cards
            self.card_count += 2
            self.current_level += 1
            self.generate_sequence()
            self.save()
        else:
            self.is_completed = True
            self.save()

    def reset_game(self):
        self.card_count = 4
        self.current_level = 1
        self.is_completed = False
        self.generate_sequence()
        self.save()

class DirectionalMemoryGame(models.Model):
    name = models.CharField(max_length=100, default="Directional Memory")
    description = models.TextField(default="Memorize and replicate the arrow sequence")
    icon = models.CharField(max_length=50, default='↔️')
    url_path = models.CharField(max_length=100, default='directional-memory')
    created_at = models.DateTimeField(auto_now_add=True)
    current_level = models.IntegerField(default=1)
    sequence_length = models.IntegerField(default=3)  # Start with 3 arrows
    arrow_sequence = models.JSONField(default=list)
    is_completed = models.BooleanField(default=False)

    ARROWS = ['↑', '→', '↓', '←']

    def generate_sequence(self):
        # Generate random sequence of arrows
        sequence = [random.choice(self.ARROWS) for _ in range(self.sequence_length)]
        self.arrow_sequence = sequence
        self.save()
        return sequence

    def increase_difficulty(self):
        if self.sequence_length < 5:  # Three levels: 3, 4, and 5 arrows
            self.sequence_length += 1
            self.current_level += 1
            self.generate_sequence()
            self.save()
        else:
            self.is_completed = True
            self.save()

    def reset_game(self):
        self.sequence_length = 3
        self.current_level = 1
        self.is_completed = False
        self.generate_sequence()
        self.save()
