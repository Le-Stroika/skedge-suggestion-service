def get_schedules(course_data: list) -> list:
    """get a list of courses and return back the same thing
    but the option map is replaced by the actual choice and return
    all of them"""


def is_conflict(c1: tuple, c2: tuple) -> bool:
    return not (c1[1] < c2[0] or c2[1] < c1[0])

# ----------------------------------------

from collections import defaultdict


def enemyDicc(dislikes):
    result = defaultdict(set)
    for a, b in dislikes:
        result[a].add(b)
        result[b].add(a)
    return result


def formGroups(dislikes, max_):
    enemiesOf = enemyDicc(dislikes)
    ppl = list(enemiesOf.keys())
    # sort by most to least hated this is a heuristic
    ppl = sorted(ppl, key=lambda x: len(enemiesOf[x]), reverse=True)
    # you want to deal with the most problematic people first
    # if you leave them for last it will be very bad
    return findFrom(ppl, {}, max_, enemiesOf)


def findFrom(people, grouping, max_, enemiesOf):
    if not people:
        # everyone is in this grouping and we are done
        return grouping
    grp_ids = set(grouping.values())
    # extra param for edge case at start
    num_grps = max(grp_ids, default=0)
    person, rest = people[0], people[1:]
    # find a group that can take this person
    for id_ in grp_ids:
        hater_in_grp = any(enemy in grouping and grouping[enemy] == id_
                           for enemy in enemiesOf[person])
        if not hater_in_grp:
            grouping[person] = id_
            next_ = findFrom(rest, grouping, max_, enemiesOf)
            if next_:
                return next_
            else:
                del grouping[person]
    # if no one can, try to make a new one
    if num_grps < max_:
        grouping[person] = num_grps + 1
        next_ = findFrom(rest, grouping, max_, enemiesOf)
        if next_:
            return next_
        else:
            del grouping[person]
    return None
