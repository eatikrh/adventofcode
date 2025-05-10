import numpy as np
import pandas as pd
from collections import defaultdict

test_small_map = False

def explore_paths(y, x, path="", visited=None):
    if visited is None:
        visited = set()
    visited.add((y, x))

    current_value = A[y, x]
    paths = []

    #print(f"---Start: y={y},  x={x},  Value={current_value}, path={path} ")
    moved = False
    for dir in ['U', 'R', 'D', 'L']:
        delta_y, delta_x = deltas[dir]

        new_y = y + delta_y
        new_x  = x + delta_x
        new_x  = x + delta_x
        #print(f"Going: {dir} delta_y={delta_y}, delta_x={delta_x}, new_y={new_y}, new_x={new_x}")

        if (
            0 <= new_y < A.shape[0]
            and 0 <= new_x < A.shape[1]
            and 0 <= y - 1 < can_move[dir].shape[0]
            and 0 <= x - 1 < can_move[dir].shape[1]
        ):
            #print(f"pre-move new_y={new_y}, new_x={new_x}, Old Value={A[y, x]} New Value={A[new_y, new_x]}, path={path}")
            if (can_move[dir][y - 1, x -1 ] == 1
            and (new_y, new_x) not in visited
            ):
                #print(f"can move: can_move[dir][y - 1, x - 1] = {can_move[dir][y - 1, x - 1]}, visited: {(new_y, new_x) in visited}")
                moved = True
                #print(f"moved=True, new_y={new_y}, new_x={new_x}, Old Value={A[y, x]} New Value={A[new_y, new_x]}, path={path}")
                new_paths = explore_paths(new_y, new_x, path + dir, visited.copy())
                paths.extend(new_paths)
            #else:
                #print(f"cannot move: can_move[dir][y - 1, x - 1] = {can_move[dir][y - 1, x -1]}, visited: {(new_y, new_x) in visited}")
        #else:
            #print(f"what is going on here? some dimension issue:  0 <= new_y < A.shape[0] { 0 <= new_y < A.shape[0]}, 0 <= new_x < A.shape[1]  {0 <= new_x < A.shape[1]  }, 0 <= y < can_move[dir].shape[0]  {0 <= y < can_move[dir].shape[0] }, 0 <= x < can_move[dir].shape[1]={ 0 <= x < can_move[dir].shape[1]} ")
            #print(f"what is going on here? some dimension issue:  new_y ={new_y}, A.shape[0]={A.shape[0]}, new_x={new_x}, A.shape[1]={A.shape[1]}")


    if not moved:
        # print(f"returning current_value={current_value}, moved={moved},  x={x}, y={y}")
        ends_at_9 = (current_value == 9)
        paths.append(((y, x), path, ends_at_9))  # include final coordinates

    return paths

# Original matrix
if test_small_map:
    A_original = np.array([
        [8, 9, 0, 1, 0, 1, 2, 3],
        [7, 8, 1, 2, 1, 8, 7, 4],
        [8, 7, 4, 3, 0, 9, 6, 5],
        [9, 6, 5, 4, 9, 8, 7, 4],
        [4, 5, 6, 7, 8, 9, 0, 3],
        [3, 2, 0, 1, 9, 0, 1, 2],
        [0, 1, 3, 2, 9, 8, 0, 1],
        [1, 0, 4, 5, 6, 7, 3, 2]
    ])


if not test_small_map:
    # Convert your large matrix string into a 2D numpy array
    matrix_str = """
    321021092121234789832103214321006541010132106541017654300
    438934783010345676543345305453217432187233477832018980211
    567015654501296489410256456569348945096544986910129871232
    456723123456987334320107567678758996898555678901236789543
    309854010987106212430198438734367987567456967432545210692
    219764110899234302341234329765210803456327876545694356781
    078743211898765671296541017891010712987818760176783543490
    165430302345610980387652132169125621076909859285432892101
    234321459654324341455678923078434018565012348396501783030
    965078968767865210564543014568742109410983467487645654121
    870165678654978109634332125989653478321474326576546553239
    743234589623089238723765223678764569436565015961038764548
    658921056712109841014894014569655234587652103876129855697
    067876549803458958965023789012345105698501212365012342786
    149989034104567567874112632101437656787432323453210031245
    238701123234789810983201543654328941095467654534509120430
    345632010345654321012317123788911032876338943210678921221
    765643101234983498765498014697802123943223458901098834569
    894356909875676543034567765656543112310110567812347721678
    018247812365889832103077896578987003451541476905456430549
    329106321458981018212186987107832128765434985876965501232
    478905450123472789567095011016541289892125676767874610541
    565210567012563665498144322123450156701010065367823789670
    984303498781014572301238983210761043214012153456910432987
    676542187692125981019345674529832980123723472347234561098
    701410096583455850128543265678745679654874781298100678121
    892323823496566767817610121060123498765965690107321789030
    765214910787665016901001438901298567543876212346496576543
    564305807879854325012312567652347345672104301454587432656
    678986706987763434325493498743656256783265420963678101765
    367210215432102521456786781234562101894378510872539819834
    456520344895601610569035690105678980123459826761223422123
    307431456784778700678124303234983456234389439870314565012
    218942349823869891233298212104572367945476512365409874303
    354654332210958398544567198703671398876532403456589701234
    763783041032141237653211003612980432345641123969676510145
    892892156543030340344509112501876521898750014878105430656
    321891067674321651225678783432985010456767625565254321787
    100765018789810787810589698343274981347898766984369930896
    235654329878910896923410587650123876210184567874378876787
    346543012897601235210401456871014985011543498965210765498
    457892126780540344323302345921001234327612321070178780301
    569234045601239653014212234834912321098501078789869691212
    678105030430548732012323100765873434323456539834054587101
    767876121521696671021234561234564565210766545743123456078
    878987437601787787430965876501259678703897832652012167569
    989096598912321096566876903412348789612345991001765078438
    870110182105431234565678912089987432541016787569894369327
    963223273676980017874987652176506501232346765456701254310
    854134564587832156983676543005218765101239894301012563210
    343065432196347847892565034114309450120340123219823472121
    212876701098256930101656123423212301239658921008768989032
    108989870187107821234587630123498418948767830119657812398
    017129871256766210187696541454567699859656543234546903457
    210034560345897654098543076501298788768501765401445498766
    325676894324388943089432185432107632103432852332332320125
    434589765410210012176501898543234543214345901021041010134
    """

    # Clean and convert to 2D integer array
    matrix_lines = [line.strip() for line in matrix_str.strip().split('\n')]
    A_original = np.array([[int(ch) for ch in line] for line in matrix_lines])
    A_original.shape


# Pad the matrix with 10s
A = np.pad(A_original, pad_width=1, mode='constant', constant_values=100)

U = np.roll(A, -1, axis=0); U[-1, :] = 0  # Up
D = np.roll(A, +1, axis=0); D[0, :] = 0   # Down
L = np.roll(A, -1, axis=1); L[:, -1] = 0  # Left
R = np.roll(A, +1, axis=1); R[:, 0] = 0   # Right

# Compute directional differences where neighbor = self + 1
diffs = {
    'U': (diff_U_A := (U - A == 1)),
    'D': (diff_D_A := (D - A == 1)),
    'L': (diff_L_A := (L - A == 1)),
    'R': (diff_R_A := (R - A == 1))
}
#print("Diffs):")
#print(diffs)


# Direction deltas
deltas = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

# All zero-valued starts (offset +1 for padding)
zero_starts = [tuple(pos + 1) for pos in np.argwhere(A_original == 0)]
print("Zero starts (in padded matrix A):")
for start in zero_starts:
    print(tuple(int(x) for x in start))

# Notice we are getting the diffs in opposite direction
can_move_up = np.roll(diffs['D'], shift=1, axis=0)
can_move_down = np.roll(diffs['U'], shift=-1, axis=0)
can_move_left = np.roll(diffs['R'], shift=1, axis=1)
can_move_right = np.roll(diffs['L'], shift=-1, axis=1)

print("A")
print(A_original)


print("can_move_down")
can_move_down = can_move_down[:-2, 1:-1]
print(can_move_down.astype(int))

print("can_move_up")
can_move_up = can_move_up[2:, 1:-1]
print(can_move_up.astype(int))

print("can move left")
can_move_left = can_move_left[1:-1, 2:]
print(can_move_left.astype(int))

print("can move right")
can_move_right = can_move_right[1:-1, :-2]
print(can_move_right.astype(int))


can_move = {
    'U': can_move_up,
    'D': can_move_down,
    'L': can_move_left,
    'R': can_move_right
}

# Calculate trailhead scores

trailhead_scores = {}
total_trail_count = 0
trail_rating_sum = 0

# From all A == 0 starts
with open("recursive_paths_from_0.txt", "w") as f:
    for start in zero_starts:
        paths = explore_paths(*start)
        endings = set()
        trail_rating = 0
        for end_coord, p, is_nine in paths:
            if is_nine:
                endings.add(end_coord)
                f.write(f"{(int(start[0]), int(start[1]))}: {p} (ends at 9: {is_nine})\n")
                print(f"{(int(start[0]), int(start[1]))}: {p} (ends at 9: {is_nine})\n")
                total_trail_count += 1
                trail_rating += 1

        score = len(endings)
        trailhead_scores[start] = score
        trail_rating_sum += trail_rating
        print(f"trail rating for :{start}  => {trail_rating}")

print(f"trail_rating_sum :{trail_rating_sum} ")
print(f"total_trail_count :{total_trail_count} ")


# Display results
print("\nTrailhead Scores:")
total = 0
for k in sorted(trailhead_scores):
    #print(f"{k}: {trailhead_scores[k]}")
    total += trailhead_scores[k]

print(f"\nSum of all trailhead scores: {total}")


