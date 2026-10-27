# ONLY a local synthetic identity switch. This is NOT production authentication.
class TrainingIdentity
  def self.resolve(header)
    return nil unless %w[operator-a operator-b].include?(header)
    Actor.find_by(handle: header, active: true)
  end
end
