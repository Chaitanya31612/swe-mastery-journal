# One valid repair

Use config.fetch(:send_email, true) to preserve false. Use Hash.new { |h,k| h[k] = [] } for separate stored buckets.

Test missing, false, and true settings. Test two distinct bucket keys and inspect keys as well as values.

**How to check:** Zero and empty containers are truthy in Ruby. Test presence and numeric rules explicitly.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.