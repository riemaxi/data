class Heatmap{
	constructor(rows, cols){
		this.rows = rows;
		this.cols = cols;
		this.data = {}
	}

	addScore(s){
		s[0] = this.reference.indexOf(s[0])
		let key = s[0] + "_" + s[1]
		let score = s[s.length-1] * 100

		this.data[key] = score
	}

	getScore(col, row, defvalue = 0){
		let score = this.data[col + "_" + row]
		return score != null?score : defvalue
	}

	update(x, y, size){
		for (let row = 0; row < this.rows; row++)
			for (let col = 0; col < this.cols; col++){
				let c1 = map(col,0,this.cols-1, x, x + size.width);
				let r1 = map(row,0,this.rows-1, y, y + size.height);
				let c2 = map(col+1,0,this.cols-1, x, x +  size.width);
				let r2 = map(row+1,0,this.rows-1, y, y + size.height);

				let color = map(this.getScore(col, row), 0, 100, 255, 0);

				fill(color);
				rect(c1, r1, c2-c1,r2 - r1);
			}
	}

	set(reference, rows){
		this.reference = reference;
		this.rows = rows;
		this.cols = this.reference.length
	}
}

class Lines{
	constructor(data){
		this.data = data != null ? data : {}

		this.size = this.data.length;
	}

	reset(size){
		this.size = size;
		this.data = {}
	}

	getScore(position, defvalue = 0){
		let score = this.data[position];
		return score != null?score : defvalue
	}

	addScore(s){
		this.data[s.position] = s.value
	}

	addAll(data){
	   this.reset(data.length);
	   for (let i=0; i < this.size; i++)
		this.addScore({ position: i, value : data[i]})
	}

	update(x, y, size){
		strokeWeight(4);
		stroke(0)

		for (let pos = 1; pos < this.size; pos++){
			let prevscore = this.getScore(pos-1);
			let score =  this.getScore(pos)

			if (isNaN(prevscore))
				continue;

			let x1 = map(pos-1, 0, this.size-1,x, x + size.width);
			let y1 = map(prevscore, 0, 100, y + size.height, y);

			if (isNaN(score))
				continue;

			let x2 = map(pos, 0, this.size-1,x, x + size.width);
			let y2 = map(score, 0, 100, y + size.height, y);

			line(x1,y1,x2,y2)

		}
	}
}


class Layout{
	constructor(xo,yo, region){
		this.region = region != null ? region : []
		this.xo = xo
		this.yo = yo

	}

	add(c){
		this.region.push(c)
	}

	update(){
		for (let i=0; i<this.region.length;i++){
			let r = this.region[i]
			r.component.update(this.xo + r.position.x, this.yo + r.position.y, r.size)
		}
	}
}
