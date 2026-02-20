"""
Negotiation simulation (alternating offers with discounting) in Pygame

Save as negotiation_pygame.py and run:
    python negotiation_pygame.py

Controls (mouse):
- Click the + / - buttons to change delta1/delta2 and max rounds
- Click Start to run the negotiation animation
- Click Reset to reset parameters

The simulation computes the subgame-perfect offers via backward induction (finite horizon)
and animates each round showing the proposer, the offer, acceptance, and final outcome.

Requires: pygame (install via pip install pygame)
"""

import pygame
import sys
import math
from dataclasses import dataclass

# ---- Model parameters ----
R = 100.0

# ---- Backward induction and simulation (same logic as prior text-based version) ----

def compute_backwards(max_rounds: int, delta1: float, delta2: float):
    S1 = [(0.0, 0.0) for _ in range(max_rounds + 2)]
    S2 = [(0.0, 0.0) for _ in range(max_rounds + 2)]
    for t in range(max_rounds, 0, -1):
        cont_v2 = S2[t + 1][1]
        denom2 = (delta2 ** (t - 1)) if delta2 > 0 else 0.0
        if denom2 > 0:
            a2_min = cont_v2 / denom2
        else:
            a2_min = float('inf')
        if a2_min <= R:
            v1 = (delta1 ** (t - 1)) * (R - a2_min)
            v2 = cont_v2
            S1[t] = (v1, v2)
        else:
            S1[t] = S2[t + 1]

        cont_v1 = S1[t + 1][0]
        denom1 = (delta1 ** (t - 1)) if delta1 > 0 else 0.0
        if denom1 > 0:
            a1_min = cont_v1 / denom1
        else:
            a1_min = float('inf')
        if a1_min <= R:
            v2 = (delta2 ** (t - 1)) * (R - a1_min)
            v1 = cont_v1
            S2[t] = (v1, v2)
        else:
            S2[t] = S1[t + 1]
    return S1, S2


@dataclass
class RoundState:
    round_no: int
    proposer: str
    offer: tuple | None
    accepted: bool


def simulate_steps(max_rounds, delta1, delta2, starter='player1'):
    S1, S2 = compute_backwards(max_rounds, delta1, delta2)
    history = []
    current = starter
    for t in range(1, max_rounds + 1):
        if current == 'player1':
            cont_v2 = S2[t + 1][1]
            denom2 = (delta2 ** (t - 1)) if delta2 > 0 else 0.0
            a2_min = cont_v2 / denom2 if denom2 > 0 else float('inf')
            if a2_min <= R:
                a2 = max(0.0, min(R, a2_min))
                a1 = R - a2
                offer = (a1, a2)
                history.append(RoundState(t, 'player1', offer, True))
                return history
            else:
                history.append(RoundState(t, 'player1', None, False))
                current = 'player2'
        else:
            cont_v1 = S1[t + 1][0]
            denom1 = (delta1 ** (t - 1)) if delta1 > 0 else 0.0
            a1_min = cont_v1 / denom1 if denom1 > 0 else float('inf')
            if a1_min <= R:
                a1 = max(0.0, min(R, a1_min))
                a2 = R - a1
                offer = (a1, a2)
                history.append(RoundState(t, 'player2', offer, True))
                return history
            else:
                history.append(RoundState(t, 'player2', None, False))
                current = 'player1'
    return history


# ---- Pygame UI ----

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Alternating Offers Negotiation (Discounting)')
FONT = pygame.font.SysFont('Arial', 18)
BIGFONT = pygame.font.SysFont('Arial', 24)
CLOCK = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHTGRAY = (230, 230, 230)
GREEN = (44, 160, 44)
RED = (214, 39, 40)
BLUE = (31, 119, 180)

# UI state
delta1 = 0.95
delta2 = 0.90
max_rounds = 15
starter = 'player1'

running_sim = False
sim_history = []
current_step_index = 0
step_timer = 0.0
STEP_DELAY = 1000  # ms between steps

# Buttons and rectangles
start_btn_rect = pygame.Rect(700, 480, 160, 40)
reset_btn_rect = pygame.Rect(700, 530, 160, 40)
plus1_rect = pygame.Rect(240, 80, 30, 30)
minus1_rect = pygame.Rect(200, 80, 30, 30)
plus2_rect = pygame.Rect(240, 140, 30, 30)
minus2_rect = pygame.Rect(200, 140, 30, 30)
plusR_rect = pygame.Rect(240, 200, 30, 30)
minusR_rect = pygame.Rect(200, 200, 30, 30)
starter_toggle_rect = pygame.Rect(200, 260, 120, 30)


def draw_text(text, x, y, font=FONT, color=BLACK):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))


def draw_ui():
    # background
    screen.fill(WHITE)
    # Title
    draw_text('Alternating-offers Negotiation (Discounted)', 20, 10, BIGFONT)

    # Parameter panel
    pygame.draw.rect(screen, LIGHTGRAY, (180, 60, 360, 260))
    draw_text('Parameters:', 190, 65, BIGFONT)
    # delta1
    draw_text('Player1 discount (delta1):', 200, 85)
    pygame.draw.rect(screen, GRAY, minus1_rect)
    draw_text('-', minus1_rect.x + 9, minus1_rect.y + 5, BIGFONT)
    pygame.draw.rect(screen, GRAY, plus1_rect)
    draw_text('+', plus1_rect.x + 8, plus1_rect.y + 5, BIGFONT)
    draw_text(f'{delta1:.4f}', 290, 85)

    # delta2
    draw_text('Player2 discount (delta2):', 200, 145)
    pygame.draw.rect(screen, GRAY, minus2_rect)
    draw_text('-', minus2_rect.x + 9, minus2_rect.y + 5, BIGFONT)
    pygame.draw.rect(screen, GRAY, plus2_rect)
    draw_text('+', plus2_rect.x + 8, plus2_rect.y + 5, BIGFONT)
    draw_text(f'{delta2:.4f}', 290, 145)

    # max rounds
    draw_text('Max rounds:', 200, 205)
    pygame.draw.rect(screen, GRAY, minusR_rect)
    draw_text('-', minusR_rect.x + 9, minusR_rect.y + 5, BIGFONT)
    pygame.draw.rect(screen, GRAY, plusR_rect)
    draw_text('+', plusR_rect.x + 8, plusR_rect.y + 5, BIGFONT)
    draw_text(f'{max_rounds}', 290, 205)

    # starter
    pygame.draw.rect(screen, GRAY, starter_toggle_rect)
    draw_text(f'Starter: {starter}', starter_toggle_rect.x + 6, starter_toggle_rect.y + 6)

    # Buttons
    pygame.draw.rect(screen, BLUE if not running_sim else GRAY, start_btn_rect)
    draw_text('Start / Run', start_btn_rect.x + 30, start_btn_rect.y + 12, FONT, WHITE if not running_sim else BLACK)
    pygame.draw.rect(screen, RED, reset_btn_rect)
    draw_text('Reset', reset_btn_rect.x + 60, reset_btn_rect.y + 12, FONT, WHITE)

    # Display negotiation panel
    pygame.draw.rect(screen, LIGHTGRAY, (20, 340, 660, 240))
    draw_text('Negotiation timeline & outcome:', 30, 345, BIGFONT)

    # If simulation has steps, draw them
    y0 = 380
    if not sim_history:
        draw_text('No simulation yet. Adjust parameters and click Start.', 30, y0)
    else:
        # show up to first 8 rounds
        for i, rs in enumerate(sim_history[:8]):
            y = y0 + i * 28
            text = f"Round {rs.round_no}: Proposer={rs.proposer}"
            if rs.offer is None:
                text += ' -> Offered nothing (rejected)'
            else:
                a1, a2 = rs.offer
                text += f' -> Offer: P1={a1:.2f}, P2={a2:.2f}'
                text += ' [ACCEPT]' if rs.accepted else ' [REJECT]'
            draw_text(text, 30, y)

    # If agreement reached, display final outcome summary to the right
    if sim_history and any(r.accepted for r in sim_history):
        # find first accepted
        accepted_rounds = [r for r in sim_history if r.accepted]
        first = accepted_rounds[0]
        a1, a2 = first.offer
        # discounted utilities based on round
        u1 = (delta1 ** (first.round_no - 1)) * a1
        u2 = (delta2 ** (first.round_no - 1)) * a2
        draw_text('Final Agreement:', 700, 60, BIGFONT)
        draw_text(f'Round: {first.round_no}', 700, 100)
        draw_text(f'Proposer: {first.proposer}', 700, 130)
        draw_text(f'Allocation: P1={a1:.4f}, P2={a2:.4f}', 700, 160)
        draw_text(f'Discounted utilities: U1={u1:.4f}, U2={u2:.4f}', 700, 190)
        fair_tol = 5.0
        if abs(a1 - R/2) <= fair_tol and abs(a2 - R/2) <= fair_tol:
            draw_text('Outcome resembles Nash-like fair (≈50-50)', 700, 220, FONT, GREEN)
        else:
            draw_text('Outcome NOT close to 50-50 (proposer advantage)', 700, 220, FONT, RED)


def run_simulation():
    global sim_history, running_sim, current_step_index, step_timer
    sim_history = simulate_steps(max_rounds, delta1, delta2, starter)
    running_sim = True
    current_step_index = 0
    step_timer = pygame.time.get_ticks()


def reset_sim():
    global sim_history, running_sim, current_step_index
    sim_history = []
    running_sim = False
    current_step_index = 0


# Helpers for button clicks

def inside(rect, pos):
    return rect.collidepoint(pos)


# Main loop

def main_loop():
    global delta1, delta2, max_rounds, starter, running_sim, current_step_index, step_timer
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if inside(start_btn_rect, pos):
                    run_simulation()
                elif inside(reset_btn_rect, pos):
                    reset_sim()
                elif inside(plus1_rect, pos):
                    delta1 = min(0.9999, delta1 + 0.01)
                elif inside(minus1_rect, pos):
                    delta1 = max(0.01, delta1 - 0.01)
                elif inside(plus2_rect, pos):
                    delta2 = min(0.9999, delta2 + 0.01)
                elif inside(minus2_rect, pos):
                    delta2 = max(0.01, delta2 - 0.01)
                elif inside(plusR_rect, pos):
                    max_rounds = min(200, max_rounds + 1)
                elif inside(minusR_rect, pos):
                    max_rounds = max(1, max_rounds - 1)
                elif inside(starter_toggle_rect, pos):
                    starter = 'player2' if starter == 'player1' else 'player1'

        # update running simulation animation by stepping through history
        if running_sim and sim_history:
            now = pygame.time.get_ticks()
            if now - step_timer >= STEP_DELAY:
                # advance to next displayed step if any; here we simply ensure the history is visible -
                # since simulate_steps returns only until agreement (or empty), we keep running_sim True
                # for a short while then stop
                current_step_index += 1
                step_timer = now
                # stop if we've shown all steps
                if current_step_index >= len(sim_history):
                    running_sim = False

        draw_ui()
        pygame.display.flip()
        CLOCK.tick(30)


if __name__ == '__main__':
    main_loop()