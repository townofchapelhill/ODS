select 
p.Num Permit_Number,
p.D_Filed Date_Filed,
p.D_Start Date_Issued,
p.Address,
p.Descr Description,
pgd.PIN,
pgd.Owner,
pgd.Contractors,
pgd.ConstrVal Cost_of_Construction,
pgd.LandUse Land_Use
	from Prmt p
join PrmtGridData pgd on p.PrmtID = pgd.PrmtID
