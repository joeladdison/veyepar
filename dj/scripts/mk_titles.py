#!/usr/bin/python

# creates svg titles for all the episodes
# used to preview the title slides,
# enc.py will re-run the same code.

from enc import enc

from main.models import Episode


class mk_title(enc):

    ready_state = None

    def process_ep(self, episode: Episode) -> bool:
        """
        Generate title images if required, and optionally display/rsync them.
        NOTE: Always returns False as the Episode state is not incremented from this action.
        """
        title_img = self.mk_title(episode)
        if not title_img:
            print(f"Failed to get title image for {episode.slug}")
            return False

        if self.options.rsync:

            if self.options.verbose:
                print("syncing {}".format(episode.slug))

            self.file2cdn(episode.show, "titles/%s.png" % (episode.slug))
            self.file2cdn(episode.show, "titles/%s.svg" % (episode.slug))

            if self.options.assets:
                self.file2cdn(episode.show, "tmp/%s.mlt" % (episode.slug))
                self.file2cdn(episode.show, "tmp/%s.sh" % (episode.slug))
                self.file2cdn(episode.show,
                        "titles/%s.svg" % (episode.slug))

            return False

        if self.options.display:
            png_name = title_img
            self.run_cmd(['display', png_name])

        return False

    def add_more_options(self, parser):
        parser.add_option('--rsync', action="store_true",
            help="upload to DS box.")
        parser.add_option('--assets', action="store_true",
            help="upload cutlist too.")
        parser.add_option('--display', action="store_true",
            help="display the png.")


if __name__ == '__main__':
    p=mk_title()
    p.main()
