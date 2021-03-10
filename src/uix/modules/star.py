class Star:
    @staticmethod
    def update_stars_from_character(char, size, poses, star_data=None):
        if star_data is None:
            star_data = {}
        if char is not None:
            for index in range(10):
                made, star = Star.make_star_with_char(star_data, char, index+1, index, size, poses)
                if made:
                    star_data[f'star_{index}'] = star
                else:
                    break
        return list(star_data.values())

    @staticmethod
    def update_stars_from_count(count, size, poses):
        star_data = {}
        for index in range(count):
            star_data[f'star_{index}'] = Star.make_star(index, size, poses[index])
        return list(star_data.values())

    @staticmethod
    def make_star(index, size, pos):
        return {'id':        f'star_{index}',
                'source':    'screens/stats/star.png',
                'broken': False,
                'size_hint': size,
                'pos_hint':  pos}

    @staticmethod
    def make_star_with_char(star_data, character, rank, index, size, poses):
        if f'star_{index}' in star_data:
            star = star_data[f'star_{index}']
        elif character.get_rank(rank).is_unlocked():
            star = Star.make_star(index, size, poses[index])
        else:
            return False, None
        if not star['broken'] and character.get_rank(rank).is_broken():
            star['source'] = 'screens/stats/rankbrk.png'
            star['broken'] = True
        return True, star
