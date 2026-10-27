# The idea

Rescue exceptions where you can add useful context or recover.

Do not turn every failure into nil. rescue without an explicit class normally catches StandardError; it does not mean every possible process failure. Catching Exception broadly can swallow interrupts and system exits.

Use block forms for files so cleanup happens when the block finishes, including on ordinary exceptions. ensure is useful for cleanup, but a return in ensure can accidentally replace the original result or failure.

Bundler selects gem versions from a Gemfile and lockfile. bundle exec runs under that dependency selection. An installed global gem is not proof of what an application uses.

Ruby threads can overlap I/O. MRI’s global VM lock limits parallel Ruby execution for CPU-bound work; it is not a database lock or a guarantee against races.