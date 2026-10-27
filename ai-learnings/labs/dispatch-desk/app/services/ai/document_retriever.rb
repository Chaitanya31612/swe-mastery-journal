module Ai
  class DocumentRetriever
    def self.call(actor:,query:,vector:nil)
      scope=PolicyDocument.visible_to(actor)
      raise InvalidResult, 'Query too large' unless query.is_a?(String) && query.length.between?(1,500)
      if vector
        raise InvalidResult, 'Invalid dimension' unless vector.is_a?(Array) && vector.length==3
        values=vector.map { |n| Float(n) }
        raise InvalidResult, 'Invalid vector' unless values.all?(&:finite?) && values.any? { |n| n!=0 }
        # Only validated numeric data enters this quoted vector literal. Never
        # use model/user SQL or identifiers in this fragment.
        literal=ApplicationRecord.connection.quote('['+values.join(',')+']')
        scope=scope.order(Arel.sql("embedding <=> #{literal}::vector"))
      else
        scope=scope.where("to_tsvector('simple', body) @@ plainto_tsquery('simple', ?)",query)
      end
      scope.limit(5).pluck(:id,:title,:source_version,:body).map { |id,title,version,body| {id:id,title:title,source_version:version,body:body} }
    rescue ArgumentError, TypeError
      raise InvalidResult, 'Invalid vector'
    end
  end
end
